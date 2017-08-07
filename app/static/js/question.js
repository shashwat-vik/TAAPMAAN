var MYTIMER, TIMER_STARTED=null;

var ontick_handler = function(ms) {
    x = String(Math.ceil(ms/1000));
    console.log(x);
    if(x.length > 1) x=x[0]+" "+x[1];
    else x="0 "+x[0];
    $('.card-timer').html("0 0 : "+x);
};

MYTIMER = new Timer({
    tick: 1,
    ontick  : function(ms) { ontick_handler(ms); },
    onend   : function() { $('.card-timer').html("0 0 : 0 0"); }
});


// PAUSE TIMER, TOGGLE LOCK SYMBOL & OPTION HIGHLIGHT CHANGE, IF LOCK CARD HAS LOCK SYMBOL
cardlock_handler = function() {
    // ACTION APPROPRIATE TO UNLOCKED STATE
    if ($(".card-lock").find(".fa-unlock").length) {
        // CHANGE SYMBOL AND PAUSE TIMER
        $(".card-lock").children('i').removeClass('fa-unlock');
        $(".card-lock").children('i').addClass('fa-lock');
        MYTIMER.pause();

        // GIVE OPTION EFFECT OF RIGHT/WRONG ANSWER
        var selection = null;
        for(var i=1; i<=4; ++i) {
            if ($("#option_"+String(i)+".option button").hasClass('border_effect neutral_answer')) {
                    selection=String(i);
            }
        }
        var answer = $(".insights .answer_option").attr("secanswer");
        $("#option_"+selection+".option button").removeClass('border_effect neutral_answer');
        if (answer == selection) {
            $("#option_"+selection+".option button").addClass('right_answer');
        } else {
            $("#option_"+selection+".option button").addClass('wrong_answer');
        }
    };
};

$(document).ready(function(e) {
    // TIMER HANDLER. ACTIVATE TIMER ON CLICK, IF NOT ALREADY TICKING.
    $(".card-header .card-timer").click(function() {
        console.log("HEADER CLICKED");
        if (!TIMER_STARTED) {
            MYTIMER.start(30);
            TIMER_STARTED=true;
        }
    });

    // LOCK CLICK HANDLER.
    $(".card-lock").on('click', cardlock_handler);

    // OPTION SELECTION HANDLER. GIVES BORDER EFFECT OVER OPTIONS.
    $(".card-options > .option").on('click', function() {
        if ($(".card-lock").find(".fa-unlock").length) {
            for(var i=1; i<=4; ++i) {
                $("#option_"+String(i)+".option button").removeClass('border_effect neutral_answer');
            }
            $(this).find('button').addClass('border_effect neutral_answer');
        }
    });

    // ENVOLOPE CLICK HANDLER
    $(".card-header .card-utils .fa-envelope-o").click(function() {
        var answer = $(".insights .answer_option").attr("secanswer");
        // // ONLY IF LIFELINE IS RIGHT ANSWER NOT ALREADY TICKED AND CARD-LOCK IS CLOSED
        if (!$("#option_"+answer+".option button").hasClass('right_answer') && $(".card-lock").find(".fa-lock").length) {
            $("#option_"+answer+".option button").addClass('right_answer');
        }
    });

    // BEGINNING LIFELINE STATUS UPDATE
    var pattern = $(".insights .lifeline_status").attr("pattern");
    var score = parseInt($(".insights .insight_score").attr("score"));
    if (pattern[0] == "0")
        $(".card-header .card-lifelines .fa-mortar-board").addClass('card-lifeline-disable');
    if (pattern[1] == "0")
        $(".card-header .card-lifelines .fa-smile-o").addClass('card-lifeline-disable');
    if (pattern[2] == "0")
        $(".card-header .card-lifelines .fa-subscript").addClass('card-lifeline-disable');
    if (pattern[3] == "0" || score < 75)
        $(".card-header .card-lifelines .fa-history").addClass('card-lifeline-disable');

    // ASSIGN LIFELINE HANDLERS
    $(".card-header .card-lifelines .fa-mortar-board").on('click', function() {     // ASK WISE GUY
        // ONLY IF LIFELINE IS ENABLED AND CARD-LOCK IS OPEN
        if (!$(this).hasClass('card-lifeline-disable') && $(".card-lock").find(".fa-unlock").length) {
            MYTIMER.pause();
            $(this).addClass('card-lifeline-disable')
        }
    });
    $(".card-header .card-lifelines .fa-smile-o").on('click', function() {          // ASK FRIEND
        // ONLY IF LIFELINE IS ENABLED AND CARD-LOCK IS OPEN
        if (!$(this).hasClass('card-lifeline-disable') && $(".card-lock").find(".fa-unlock").length) {
            MYTIMER.pause();
            $(this).addClass('card-lifeline-disable');
        }
    });
    $(".card-header .card-lifelines .fa-subscript").on('click', function() {        // DOUBLE TAKE
        // ONLY IF LIFELINE IS ENABLED AND CARD-LOCK IS CLOSED
        if (!$(this).hasClass('card-lifeline-disable') && $(".card-lock").find(".fa-lock").length) {
            $(".card-lock").children('i').removeClass('fa-lock');
            $(".card-lock").children('i').addClass('fa-unlock');
            $(this).addClass('card-lifeline-disable');
            // NO NEED TO PAUSE TIMER, AS COMING HERE ALREADY IMPLIES THAT ITS PAUSED
        }
    });
});
