const showNotifications = () =>
{
    $.ajax({
        type: "GET",
        url: "/user/headernotifications",
        success: function (result) {
            data = JSON.parse(result.data);
            elms = "";
            console.log("The data : ",data);
            elms += `
                <div class="notification-box noti">
                    <div class="nt-title">
                        <h4>Setting</h4>
                        <a href="#" title="">Clear all</a>
                    </div>
                    <div class="nott-list">
            `;
            for (noti in data)
            {
                elms += `<div class="notfication-details">
                            <div class="noty-user-img">
                                <img src="" alt="">
                            </div>
                            <div class="notification-info">
                                <h3><a href="#" title=""></a> ${data[noti].fields.message}</h3>
                                <span>2 min ago</span>
                            </div><!--notification-info -->
                        </div>
                        `;
            }

            elms += `
                        <div class="view-all-nots">
                            <a href="{%url 'notification'%}" title="">View All Notification</a>
                        </div>
                    </div><!--nott-list end-->
                </div><!--notification-box end-->
            `;
            // $('#notifications').popover({
            //   content: elms
            // });
            document.getElementById('notification').innerHTML=elms;
        },
        error: function () {
            console.log(false);
        }
    });
}