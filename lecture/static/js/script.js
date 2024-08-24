let navbar = document.querySelector(".header .navbar");
document.querySelector("#menu-btn").onclick = ()=>{
navbar.classList.toggle("active");
};

document.querySelector(".header .navbar").onclick = ()=>{
navbar.classList.remove("active");
};

var swiper = new Swiper(".review-slider",{
	spaceBetween:20,
	centeredSlides:true,
	grabCursor:true,
	autoplay:{
		delay:7500,
		disableOnInteraction:false,
	},
	loop:true,
	breakpoints:{
		0:{
			slidesPerView:1,
		},

		768:{
			slidesPerView:2,
		},

		991:{
			slidesPerView:3,
		},
	}
});

$(document).ready(function(){
    var activeDiv = 1;
    showDiv(activeDiv);
    var timer = setInterval(changeDiv, 3000);

    function changeDiv(){
        activeDiv++;
        if (activeDiv ==7){
            activeDiv =1;
        }
        showDiv(activeDiv);
    }

    function showDiv(num){
        $('div.hidden').hide();
        $('#div' + num).fadeIn();
    }
})


setTimeout(fade_out, 2000)
      function fade_out(){
        $(".alert").fadeOut().empty()
      };

 $(function(){
 	$.fx.interval  = 0;
 	(function cycleBgImage(elem, bgimg){
 		elem.css("backgroundImage", bgimg)
 		.fadeTo(2000, 1, "linear", function(){
 			$(this).delay(2000, "fx").fadeTo(2000, 0, "linear", function(){
 				var img = $(this).css("backgroundImage").split(","),
 				bgimg = img.concat(img[0]).splice(1).join(",");
 				cycleBgImage(elem, bgimg);
 			});
 		});
 	}($(".home")));
 });


$("input").addClass('box');
$("textarea").addClass('box');
 $("#id_name").attr("placeholder", "Type your Name..");
 $("#id_email").attr("placeholder", "Email Address..");
 $("#id_message").attr("placeholder", "Type your Message..");


var notificationBar = document.querySelector('.notification-bar');
var notificationBarHeight = notificationBar.offsetHeight;

window.addEventListener('scroll', function(){
	var scrollPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;

	if (scrollPosition >= notificationBarHeight){
		notificationBar.classList.add('sticky');
	} else{
		notificationBar.classList.remove('sticky')
	}
});


let popup = document.getElementById("popup");

function openPop(){
    popup.classList.add("open-popup")
}

function closePop(){
    popup.classList.remove("open-popup")
}
