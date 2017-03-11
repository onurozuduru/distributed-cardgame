console.log("It works");

var host = "http://localhost:5000";

$.getJSON(host+'/newgame').done(function (data) {
    alert(JSON.stringify(data));
})
    .error(function (error) {
    alert("error");
});

