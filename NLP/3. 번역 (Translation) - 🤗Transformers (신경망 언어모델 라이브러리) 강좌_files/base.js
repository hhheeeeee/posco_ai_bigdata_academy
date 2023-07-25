$(document).ready(function () {
    $("#home_btn").click(function() {
       location.href = "/";
    });

    $("#login_btn").click(function() {
       location.href = "/loginForm";
    });

    $("#logout_btn").click(function() {
       location.href = "/logout";
    });

    $("#admin_btn").click(function() {
       location.href = "/admin";
    });

    $('.sidebar').on( 'mousewheel DOMMouseScroll', function (e) {
      var e0 = e.originalEvent;
      var delta = e0.wheelDelta || -e0.detail;

      this.scrollTop += ( delta < 0 ? 1 : -1 ) * 30;
      e.preventDefault();
    });

    $("#toggle_toc_btn").click(function () {
        if($(".toc-checker").is(":visible")) {
            $(".toc-checker").hide();
        }else {
            $(".toc-checker").removeClass("hide");
            $(".toc-checker").show();
        }
    });

    if (typeof(Storage) !== "undefined") {
        localStorage.removeItem("google_ama_config");
    }
});


/*
function recommend_book(book_id) {
    var msg = [];
    msg.push('<div class="alert alert-info">');
    msg.push('<p><strong>책을 추천합니다.</strong></p>');
//    msg.push('<p>취소는 불가능하니 신중한 추천 부탁드립니다.<br />');
    msg.push('정말로 추천하시겠습니까?</p>');
    msg.push('</div>');
    msg.push('<span class="muted">※ 추천취소는 불가능합니다.</span>');

    apprise(msg.join(''), {'verify':true}, function(r) {
        if(r) {
            location.href = "/book/recommend/"+book_id;
        }
     });
    return;
}
*/

