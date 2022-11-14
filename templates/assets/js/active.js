
function attack_target() {
    var wifi_id = document.getElementById(id)
    $(document).ready(function () {
        $("button").click(function () {
            $.ajax({
                url: "/attack/start/1/'", success: function (result) {
                    alert(result)
                }
            });
        });
    });
}