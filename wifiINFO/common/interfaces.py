import subprocess
import time

import pyric.pyw as pyw
import pyric
import logging
import random
from subprocess import PIPE, Popen

logger = logging.getLogger("wifiINFO.interfaces")


class InvalidInterfaceError(Exception):
    """ Exception class to raise in case of a invalid interface """

    def __init__(self, interface_name, mode=None):
        """
        Construct the class

        param self: A InvalidInterfaceError object
        :param interface_name: Name of an interface
        :type self: InvalidInterfaceError
        :type interface_name: str
        :return: None
        :rtype: None
        """

        message = "The provided interface \"{0}\" is invalid!".format(
            interface_name)

        # provide more information if mode is given
        if mode:
            message += "Interface {0} doesn't support {1} mode".format(
                interface_name, mode)

        Exception.__init__(self, message)


class InvalidMacAddressError(Exception):
    """
    Exception class to raise in case of specifying invalid mac address
    """

    def __init__(self, mac_address):
        """
        Construct the class

        param self: A InvalidMacAddressError object
        :param mac_address: A MAC address
        :type self: InvalidMacAddressError
        :type mac_address: str
        :return: None
        :rtype: None
        """
        message = "The MAC address could not be set. (Tried {0})".format(mac_address)
        Exception.__init__(self, message)


class InvalidValueError(Exception):
    """
    Exception class to raise in case of a invalid value is supplied
    """

    def __init__(self, value, correct_value_type):
        """
        Construct the class

        param self: A InvalidValueError object
        :param value: The value supplied
        :param correct_value_type: The correct value type
        :type self: InvalidValueError
        :type value: any
        :type correct_value_type: any
        :return: None
        :rtype: None
        """

        value_type = type(value)

        message = ("Expected value type to be {0} while got {1}.".format(
            correct_value_type, value_type))
        Exception.__init__(self, message)


class InterfaceCantBeFoundError(Exception):
    """
    Exception class to raise in case of a invalid value is supplied
    """

    def __init__(self, interface_modes):
        """
        Construct the class

        param self: A InterfaceCantBeFoundError object
        :param interface_modes: Modes of interface required
        :type self: InterfaceCantBeFoundError
        :type interface_modes: tuple
        :return: None
        :rtype: None
        .. note: For interface_modes the tuple should contain monitor
            mode as first argument followed by AP mode
        """

        monitor_mode = interface_modes[0]
        ap_mode = interface_modes[1]

        message = "Failed to find an interface with "

        # add appropriate mode
        if monitor_mode:
            message += "monitor"
        elif ap_mode:
            message += "AP"

        message += " mode"

        Exception.__init__(self, message)


class InterfaceManagedByNetworkManagerError(Exception):
    """
    Exception class to raise in case of NetworkManager controls the AP or deauth interface
    """

    def __init__(self, interface_name):
        """
        Construct the class.
        :param self: An InterfaceManagedByNetworkManagerError object
        :param interface_name: Name of interface
        :type self: InterfaceManagedByNetworkManagerError
        :type interface_name: str
        :return: None
        :rtype: None
        """

        message = (
            "Interface \"{0}\" is controlled by NetworkManager."
            "You need to manually set the devices that should be ignored by NetworkManager "
            "using the keyfile plugin (unmanaged-directive). For example, '[keyfile] "
            "unmanaged-devices=interface-name:\"{0}\"' needs to be added in your "
            "NetworkManager configuration file.".format(interface_name))
        Exception.__init__(self, message)


class NetworkAdapter(object):
    """ This class represents a network interface """

    def __init__(self, name, card, mac_address):
        """
        Setup the class with all the given arguments

        :param self: A NetworkAdapter object
        :param name: Name of the interface
        :param card: A pyric.pyw.Card object
        :param mac_address: The MAC address of interface
        :type self: NetworkAdapter
        :type name: str
        :type card: pyric.pyw.Card
        :type mac_address: str
        :return: None
        :rtype: None
        """
        # Setup the fields
        self._name = name
        self._card = card
        self._mac_address = mac_address
        self._is_managed_by_nm = False
        # self._has_master_mode = False
        # self._has_monitor_mode = False
        self.init_mode()
        # self._original_mac_address = mac_address
        # self._current_mac_address = mac_address

    def init_mode(self):
        subprocess.Popen([
            'airmon-ng',
            'start',
            self.name
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def up(self):
        """
        Equivalent to ifconfig interface up

        :param self: A NetworkAdapter object
        :type self: Interface
        :return: None
        :rtype: None
        ..note: 启动接口
        """

        pyw.up(self._card)

    def down(self):
        """
        Equivalent to ifconfig interface down

        :param self: A NetworkAdapter object
        :type self: Interface
        :return: None
        :rtype: None
        ..note: 关闭接口
        """
        pyw.down(self._card)

    def is_managed_by_nm(self, value):
        """
        Set whether the interface is controlled by NetworkManager

        :param self: A NetworkAdapter object
        :param value: A value representing interface controlled by NetworkManager
        :type self: NetworkAdapter
        :type value: bool
        :return: None
        :rtype: None
        :raises InvalidValueError: When the given value is not bool
        """

        if isinstance(value, bool):
            self._is_managed_by_nm = value
        else:
            raise InvalidValueError(value, bool)

    @staticmethod
    def nm_unmanage(interface):
        """
        Set an interface to unmanaged.
        :param interface: Name of the interface
        :type interface: str
        :return: True upon success
        :rtype: bool
        """
        try:
            proc = Popen(['nmcli', 'dev', 'set', interface, 'manage', 'no'], stderr=PIPE)
            err = proc.communicate()[1]
        except:
            logger.error("Failed to make NetworkManager unmanage interface {0}: {1}".format(interface, err))
            raise InterfaceManagedByNetworkManagerError(interface)
        # Ensure that the interface is unmanaged
        if is_managed_by_network_manager(interface):
            raise InterfaceManagedByNetworkManagerError(interface)

    def get_interface_mac(self):
        """
        Return the MAC address of the interface

        :param self: A NetworkAdapter object
        :type self: NetworkAdapter
        :return: Interface MAC address
        :rtype: str
        """

        return self._mac_address

    def set_interface_mac(self, mac_address=None):
        """
        Set the specified MAC address for the interface

        :param self: A NetworkAdapter object
        :param mac_address: A MAC address
        :type self: NetworkAdapter
        :type mac_address: str
        :return: new MAC
        :rtype: str
        .. note: This method will set the interface to master mode
        """

        if not mac_address:
            mac_address = generate_random_address()

        self._mac_address = mac_address
        card = self._card
        self.set_interface_mode("master")

        self.down()
        # card must be turned off(down) before setting mac address
        try:
            pyw.macset(card, mac_address)
        # make sure to catch an invalid mac address
        except pyric.error as error:
            raise InvalidMacAddressError(mac_address)
        return mac_address

    def set_interface_mode(self, mode):
        """
        Set the specified mode for the interface

        :param self: A NetworkAdapter object
        :param mode: Mode of an interface
        :type self: NetworkAdapter
        :type mode: str
        :return: None
        :rtype: None
        .. note: Available modes are unspecified, ibss, managed, AP
            AP VLAN, wds, monitor, mesh, p2p
            Only set the mode when card is in the down state
        """
        mode_list = ['managed', 'master', 'monitor', 'ad-hoc']
        if mode.lower() not in mode_list:
            raise ValueError

        card = self._card
        self.down()
        # set interface mode between brining it down and up
        try:
            # pyw.modeset(card, mode.lower())
            subprocess.Popen([
                'iwconfig',
                card.dev,
                'mode',
                mode
            ])
            time.sleep(5)
        except SystemError:

            raise SystemError

    @property
    def name(self):
        return self._name

    @property
    def mac(self):
        return self._mac_address

    @property
    def card(self):
        return self._card


def is_managed_by_network_manager(interface_name):
    """
    Check if the interface is managed by NetworkManager
    At this point NetworkManager may or may not be running.
    If it's not running, nothing is returned.

    :param interface_name: An interface name
    :type interface_name: str
    :return if managed by NetworkManager return True
    :rtype: bool
    """

    is_managed = False
    try:
        nmcli_process = Popen(['/bin/sh', '-c', 'export LC_ALL=C; nmcli dev; unset LC_ALL'],
                              stdout=subprocess.DEVNULL,
                              stderr=PIPE)
        out, err = nmcli_process.communicate()

        if err == None and out != "":
            for l in out.splitlines():
                # TODO: If the device is managed and user has nmcli installed,
                # we can probably do a "nmcli dev set wlan0 managed no"
                if interface_name in l:
                    if "unmanaged" not in l:
                        is_managed = True
                else:
                    # Ignore until we make handle logging registers properly.
                    pass
                    # logger.error("Failed to make NetworkManager ignore interface %s", interface_name)
        else:
            # Ignore until we make handle logging registers properly.
            pass
            # logger.error("Failed to check if interface %s is managed by NetworkManager", interface_name)

        nmcli_process.stdout.close()

    # NetworkManager service is not running so the devices must be unmanaged
    # (CalledProcessError)
    # Or nmcli is not installed...
    except:
        pass

    return bool(is_managed)


def is_wireless_interface(interface_name):
    """
    Check if the interface is wireless interface

    :param interface_name: Name of an interface
    :type interface_name: str
    :return: True if the interface is wireless interface
    :rtype: bool
    """

    if pyw.iswireless(interface_name):
        return True
    return False


def generate_random_address():
    """
    Make and return the randomized MAC address

    :return: A MAC address
    :rtype str
    .. warning: The first 3 octets are 00:00:00 by default
    """

    mac_address ="{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return mac_address


def does_have_mode(interface, mode):
    """
    Return whether the provided interface has the mode

    :param interface: Name of the interface
    :param mode: Mode of operation
    :type interface: str
    :type mode: str
    :return: True if interface has the mode and False otherwise
    :rtype: bool
    :Example:

        >>> does_have_mode("wlan0", "AP")
        True

        >>> does_have_mode("wlan1", "monitor")
        False
    """
    card = pyric.pyw.getcard(interface)

    return mode in pyric.pyw.devmodes(card)