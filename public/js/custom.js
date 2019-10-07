$(document).ready(function(){



    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:3,
        nav:true,
        center: true,
        pagination:false,
        navigation:true
        /*responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:5
            }
        }*/
    });
    var $mslide = $(".single-item");

    $mslide.slick({

        dots: false,
        arrows: false,
/*        prevArrow: '<i class="fa fa-chevron-circle-left"></i>',
        nextArrow: "<i class='fa fa-chevron-circle-right'></i>",
       autoplay: false,
*/        infinite: false,
        slidesToShow: 6

/*        autoplaySpeed: 1000*/
    });

    $('.single-item').on('beforeChange', function(event, slick, currentSlide, nextSlide){
      alert("Next Slide: " + nextSlide);
    });

    $('.toast').on('show.bs.toast', function () {
      // do something…
    });

    $('.toast').toast('show');

    startTime();
});

    var pos = 0;

    function slickChangeNext(){

        if(pos < -605){
            pos = 0;
        }
        pos -= 121;
        var attrval = 'opacity: 1; width: 2420px; transform: translate3d('+ pos +'px, 0px, 0px)';

        //alert(attrval);
        $(".single-item .slick-list .slick-track").attr('style',attrval);


    }

    function slickChangePrev(){

        if(pos < 0){
            pos += 121;
        }

         if(pos > 0){
            pos = 0;
        }

         var attrval = 'opacity: 1; width: 2420px; transform: translate3d('+ pos +'px, 0px, 0px)';

        //alert(attrval);
        $(".single-item .slick-list .slick-track").attr('style',attrval);
    }


    var sysdate = new Date();

function startTime() {

    var today = new Date();
    //alert(today.toTimeString());
    var h = today.getHours();// - (1*5);
    var m = today.getMinutes();
    var s = today.getSeconds();

    h = checkTime(h);

    var a = h >= 12 ? ' p.m.' : ' a.m.';

    h = h % 12;
    h = h ? h : 12;

    m = checkTime(m);

    s = checkTime(s);

    $("#server_time").html(h + ":" + m + a);
    var t = setTimeout(startTime, 500);

}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}