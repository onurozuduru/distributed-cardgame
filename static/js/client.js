var host = "http://localhost:5000";

var game = {
    number: -1,
    currentPlayer: "",
    hand: [],
    lastMove: "",
    points: 0,
    round: 0,
    stage: "",
    thisPlayer: "",
    currentStatus: "" //waitingForJoininingTheOtherPlayer, play
}

var updateGameStatusInterval;

$("#player1PlayedCard").hide();
$("#player2PlayedCard").hide();
$("#gameResult").hide();
$("#card1").hide();
$("#card2").hide();
$("#card3").hide();

$("#newGame").click(function(){
    game.number = -1;
    game.currentPlayer ="";
    game.hand = [];
    game.lastMove = "";
    game.points = 0;
    game.round = 0;
    game.stage = "";
    game.thisPlayer = "";
    game.currentStatus = "";

    clearInfoPanel();
    $.getJSON(host+'/newgame').done(function (data) {
        //alert(JSON.stringify(data));
        game.number = data.game_num;
        game.thisPlayer = data.player.name;
        game.hand = data.player.hand;
        game.currentStatus = "waitingForJoininingTheOtherPlayer";
        $("#player1PlayedCard").hide();
        $("#player2PlayedCard").hide();
        $("#gameResult").hide();
        $("#card1").show();
        $("#card2").show();
        $("#card3").show();     
        $("#card1").text(game.hand[0]);
        $("#card2").text(game.hand[1]);
        $("#card3").text(game.hand[2]);

        updateGameStatusInterval = setInterval(updateGameStatus, 2000);  //each 2sec
    })
        .error(function (error) {
        alert("error");
    });
})

$("#card1").click(function(){
    if(game.number<0) {$("#infoPanel").text("Start a New Game!");}
    else{checkStatusMoveCard(1);}
})

$("#card2").click(function(){
    if(game.number<0) {$("#infoPanel").text("Start a New Game!");}
    else{checkStatusMoveCard(2);}
})

$("#card3").click(function(){
    if(game.number<0) {$("#infoPanel").text("Start a New Game!");}
    else{checkStatusMoveCard(3);}
})

//functions-----------------------------------------------------------------------
function clearInfoPanel(){
    $("#infoPanel").text("");
}

function checkStatusMoveCard(i){
    $.getJSON(host+'/game/'+game.number).done(function (data) {
        //check second player has joined
        if (data.current_player == null){
            $("#infoPanel").text("No one has not joined the game yet!");
        }
        else{
            game.currentPlayer = data.current_player.name;
            if(game.currentPlayer == game.thisPlayer) {moveCard(i);}
            else{$("#infoPanel").text("It is not your turn to play!");}
        }
    }).error(function (error) {alert("error"); });
}

function moveCard(i){
    $.getJSON(host+'/move/'+game.number+'/'+game.thisPlayer+'/'+game.hand[i-1]).done(function (data) {
        game.stage = data.stage;      
        switch(i){
        case 1:
            $("#card1").hide();
            $("#player1PlayedCard").show();
            $("#player1PlayedCard").text(game.hand[0]);
            break;
        case 2:
            $("#card2").hide();
            $("#player1PlayedCard").show();
            $("#player1PlayedCard").text(game.hand[1]);
            break;
        case 3:
            $("#card3").hide();
            $("#player1PlayedCard").show();
            $("#player1PlayedCard").text(game.hand[2]);
            break;
        }
        if (game.stage == 'END') {game.currentStatus = "play";}
        }).error(function (error) {alert("error"); });
}

function showWinner(){
    $.getJSON(host+'/game/'+game.number+'/winner').done(function (data) {
        $("#player1PlayedCard").hide();
        $("#player2PlayedCard").hide();
        $("#gameResult").show();
        if (data.winner == "NO_ONE") {
            $("#gameResult").html("Endded in a tie! " + '&nbsp&nbsp' + " :|");
        }
        else if(data.winner.name == game.thisPlayer){
            $("#gameResult").html("You Win! " + '&nbsp&nbsp' +   " :)");
        }
        else{
            $("#gameResult").html("You Lost!" +  '&nbsp&nbsp' +   " :(");
        }

        clearInterval(updateGameStatusInterval);
    })
        .error(function (error) {
        alert("error");
    });
}

function updateGameStatus(){
    $.getJSON(host+'/game/'+game.number).done(function (data) {
        if (data.current_player != null){
            game.currentPlayer = data.current_player.name;
            game.stage = data.stage; 
            game.round = data.round;
            //the other player is joined
            if (game.currentStatus == "waitingForJoininingTheOtherPlayer"){
                clearInfoPanel();
            }
            //the other player played
            if(game.currentPlayer == game.thisPlayer){
                clearInfoPanel();
            }
            //show the other palyer's played card
            if(game.thisPlayer == 'p1'){
                if((game.round == 1) && (game.currentPlayer == 'p2')) {$("#player2PlayedCard").show();}
                if((game.round == 1) && (game.currentPlayer == 'p1')) {$("#player1PlayedCard").hide();}
                if((game.round == 2) && (game.currentPlayer == 'p1')) {
                    $("#player2PlayedCard").hide();
                    $("#player1PlayedCard").hide();
                }
                if((game.round == 2) && (game.stage == 'END')) {$("#player2PlayedCard").show();}
            }
            else{
                if((game.round == 0) && (game.currentPlayer == 'p2')) {$("#player2PlayedCard").show();}
                if((game.round == 1) && (game.currentPlayer == 'p2')) {
                    $("#player2PlayedCard").hide();
                    $("#player1PlayedCard").hide();
                }
                if((game.round == 2) && (game.currentPlayer == 'p1')) {$("#player2PlayedCard").show();}
                if((game.round == 2) && (game.currentPlayer == 'p2')) {$("#player1PlayedCard").hide();}
            }
            //the game is Endded
            if (game.stage == 'END') {showWinner();}
        } 
    }).error(function (error) {alert("error"); });
}