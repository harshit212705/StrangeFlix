$('document').on('resize', function (e) {
   var adjust = $('.player-wrapper').css('height');
   var hd = $('.ser-hd').css('height');
   adjust = parseInt(adjust) - parseInt(hd);
   $('.vid-cont').css('height', adjust);
});
var adjust = $('.player-wrapper').css('height');
var hd = $('.ser-hd').css('height');
adjust = parseInt(adjust) - parseInt(hd);
$('.vid-cont').css('height', adjust);

// theatre mode 

$('.theatre__button').on('click', function (e) {
   var chk = $('.theatre__button').attr('class');
   if (chk == 'theatre__button') {
      $('.playlist-container').css('display', 'none');
      $('.c-visible-t-mode').css('display', 'block');
      $('.player-wrapper').attr('class', 'col-xl-12 col-lg-12 col-md-12 player-wrapper');
      $('.theatre__button').attr('class', 'theatre__button hellooo');
      $('.video-body').css('padding', '0% 13%');
   } else {
      $('.playlist-container').css('display', 'block');
      $('.c-visible-t-mode').css('display', 'none');
      $('.player-wrapper').attr('class', 'col-xl-9 col-lg-8 col-md-7 player-wrapper');
      $('.theatre__button').attr('class', 'theatre__button');
      $('.video-body').css('padding', '0% 9%');
   }
});



// function to toggle Login modal
$('#signup').on('click', function () {
   $('#loginModal').modal('toggle')
});
$('#login').on('click', function () {
   $('#signupModal').modal('toggle')
});



// class to manage next and prevs of buttons

class DoublyLinkedList {
   constructor() {
      this.head = null;
      this.tail = null;
      this.length = 0;
   }
   insert(data, position = this.length) {
      let node = new this.Node(data);
      // List is currently empty
      if (this.head === null) {
         this.head = node;
         this.tail = node;
         this.length++;
         return this.head;
      }
      // Insertion at head
      if (position == 0) {
         node.prev = null;
         node.next = this.head;
         this.head.prev = node;
         this.head = node;
         return this.head;
      }
      let iter = 1;
      let currNode = this.head;
      while (currNode.next != null && iter < position) {
         currNode = currNode.next;
         iter++;
      }
      // Make new node point to next node in list
      node.next = currNode.next;
      // Make next node's previous point to new
      if (currNode.next != null) {
         currNode.next.prev = node;
      }
      // Make our node point to previous node
      node.prev = currNode;

      // Make previous node's next point to new node
      currNode.next = node;

      // check if inserted element was at the tail, if yes then make tail point to it
      if (this.tail.next != null) {
         this.tail = this.tail.next;
      }
      this.length++;
      return node;
   }
   remove(data, position = 0) {
      if (this.length === 0) {
         console.log("List is already empty");
         return;
      }
      this.length--;
      let currNode = this.head;
      if (position <= 0) {
         this.head = this.head.next;
         this.head.prev = null;
      } else if (position >= this.length - 1) {
         this.tail = this.tail.prev;
         this.tail.next = null;
      } else {
         let iter = 0;
         while (iter < position) {
            currNode = currNode.next;
            iter++;
         }
         currNode.next = currNode.next.next;
         currNode.next.prev = currNode;
      }
      return currNode;
   }
   display() {
      let currNode = this.head;
      while (currNode != null) {
         console.log(currNode.data + " <-> ");
         currNode = currNode.next;
      }
   }
}

DoublyLinkedList.prototype.Node = class {
   constructor(data) {
      this.data = data;
      this.next = null;
      this.prev = null;
   }
};

var playerVid = new DoublyLinkedList();

// when clicked on prev or next button get the next value in the linked list ad run it on the player
window.addEventListener('load',function(e){
  $('#pl-vid').children('li').each(function(){
     $(this).children('a').each(function(){
        playerVid.insert(this);
     });
  })
  let currNode=playerVid.head;
  while(currNode!=null){
   console.log(currNode.data);
   currNode=currNode.next;
  }
})


// load video when clicked on a video


// search by name and tag

$('#sear-by-nam').on('click', function (e) {
   $('#sear').attr('placeholder', 'search by name');
})

$('#sear-by-tag').on('click', function (e) {
   $('#sear').attr('placeholder', 'search by tag');
})




// carousel
$('#movie-controls').on('slid.bs.carousel', '', function () {
   //ajax here to load the series and movies
   var $this = $(this);
   $this.children('#movie-controls .carousel-control-prev').show();
   $this.children('#movie-controls .carousel-control-next').show();
   if ($('#movie-controls .carousel-inner .carousel-item:first').hasClass('active')) {
      $this.children('#movie-controls .carousel-control-prev').hide();
   } else if ($('#movie-controls .carousel-inner .carousel-item:last').hasClass('active')) {
      $this.children('#movie-controls .carousel-control-next').hide();
   }
});
$('#series-controls').on('slid.bs.carousel', '', function () {
   var $this = $(this);
   $this.children('#series-controls .carousel-control-prev').show();
   $this.children('#series-controls .carousel-control-next').show();
   if ($('#series-controls .carousel-inner .carousel-item:first').hasClass('active')) {
      $this.children('#series-controls .carousel-control-prev').hide();
   } else if ($('#series-controls .carousel-inner .carousel-item:last').hasClass('active')) {
      $this.children('#series-controls .carousel-control-next').hide();
   }
});
$('#free-video-controls').on('slid.bs.carousel', '', function () {
   var $this = $(this);
   $this.children('.carousel-control-prev').show();
   $this.children('.carousel-control-next').show();
   if ($('.carousel-inner .carousel-item:first').hasClass('active')) {
      $this.children('.carousel-control-prev').hide();
   } else if ($('.carousel-inner .carousel-item:last').hasClass('active')) {
      $this.children('.carousel-control-next').hide();
   }
});


// rating

var listItem = [];
var rating = 0;
$('.rating-val').each(function (e) {
   listItem.push(this);
   $(this).on('click', function (e) {
      for (var ind in listItem) {
         $(listItem[ind]).css('color', 'white');
      }
      var val = $($(this)).attr('value');
      val = parseInt(val);
      rating = val;
      for (var ind in listItem) {
         $(listItem[ind]).css('color', 'red');
         if (ind == val - 1) {
            break;
         }
      }
   })
})


$('#rate-submit').on('click', function (e) {
   console.log(rating);
   //got the rating ajax call to save it in the database
})



// comment full show
$('.show-mr-button').on('click',function(e){
   // console.log($('.show-mr-button').text().trim());
   if($('.show-mr-button').text().trim()=='show'){
      $('.d-cent').css('display','block');
      $('.show-mr-button').text('hide');
   }
   else
   {
      $('.d-cent').css('display','-webkit-box');
      $('.show-mr-button').text('show');
   }
})