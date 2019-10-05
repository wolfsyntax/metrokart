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
