// const btnLoad = document.getElementById("btnLoadMore")
// const itemsBox = document.getElementById("itemsBox")
// let visible = 5
// const handleData = () =>{
//     $.ajax({
//         type:'GET',
//         url:`/items-json/${visible}/`,
//         success:function(response){
//             console.log(response.max_size)
//             const data = response.items
//             max_size = response.max_size
//             setTimeout(()=>{
//                 data.map(item=>{
//                     console.log(item.id)
//                     console.log(item.image.url)
//                     itemsBox.innerHTML+=`
//                     ${item.image.url ? "1" : "2"}
//                     `
//                 })
//             },250)
//         },
//         error:function(error){
//             console.log(error)
//         }
//     })
// }
// handleData()
// btnLoad.addEventListener('click',()=>{
//     visible+=5
//     handleData()
// })