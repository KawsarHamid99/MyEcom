$('#slider1, #slider2, #slider3,#slider4,#slider5').owlCarousel({
    loop: true,
    margin: 2,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        320: {
            items: 2,
            nav: false,
            autoplay: false,
            
        },
        600: {
            items: 3,
            nav: true,
            autoplay: false,
        },
        1000: {
            items: 7,
            nav: true,
            loop: true,
            autoplay: false,
        }
    }
})



$('.plus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var psize = $(this).attr('psize').toString();
    var pcolor = $(this).attr('pcolor').toString();
    var eml = this.parentNode.children[2]
    console.log(id);
    
    console.log(eml);
    console.log(psize);
    console.log(pcolor);

    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id,
            prod_size:psize,
            prod_color:pcolor
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            document.getElementById("total_cost").innerText = data.total_cost
        }
    })
})


$('.minus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var psize = $(this).attr('psize').toString();
    var pcolor = $(this).attr('pcolor').toString();
    var eml = this.parentNode.children[2]
    console.log(id)

    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id,
            prod_size:psize,
            prod_color:pcolor
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            document.getElementById("total_cost").innerText = data.total_cost
        }
    })
})




$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var psize = $(this).attr('psize').toString();
    var pcolor = $(this).attr('pcolor').toString();
    var eml= this

    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id,
            prod_size:psize,
            prod_color:pcolor
        },
        success:function(data){
            console.log("Delete")
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount     

            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})