var MYTIMER, TIMER_STARTED=null;
var CURR_SCORE=null, NEW_SCORE=null, LPAT=null;

var ontick_handler = function(ms) {
    x = String(Math.ceil(ms/1000));
    if(x.length > 1) x=x[0]+" "+x[1];
    else x="0 "+x[0];
    $('.card-timer').html("0 0 : "+x);
};

MYTIMER = new Timer({
    tick: 1,
    ontick  : function(ms) { ontick_handler(ms); },
    onend   : function() { $('.card-timer').html("0 0 : 0 0"); cardlock_handler(); }
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
        var answer = $(".insights .ANS_OPT").attr("secanswer");
        answer = (answer.trim()).toLowerCase();

        if (selection != null) {
            // FOR TYPE 1
            $("#option_"+selection+".option button").removeClass('border_effect neutral_answer');
        } else {
            // FOR TYPE 2
            $(".card-input .content").removeClass('border_effect neutral_answer');
            selection = $(".card-input .content").val();
            selection = (selection.trim()).toLowerCase();
        }

        if (answer == selection) {
            $("#option_"+selection+".option button").addClass('right_answer');  // FOR TYPE 1
            $(".card-input .content").addClass('right_answer');                 // FOR TYPE 2
            update_newscore(true);
        } else {
            $("#option_"+selection+".option button").addClass('wrong_answer');  // FOR TYPE 1
            $(".card-input .content").addClass('wrong_answer');                 // FOR TYPE 2
            update_newscore(false);
        }
    };
};

// WOULD BE RAISED BY CARD-LOCK HANDLER FOR BOTH CORRECT AND FALSE
var update_newscore = function(correct) {
    curr_score = parseInt($(".insights .CURR_SCORE").attr('score'));
    level = parseInt($(".insights .LEVEL").attr('level'));
    double_half = $(".insights .DOUBLE_HALF").attr('status');
    console.log(double_half);
    if (correct) {
        NEW_SCORE = 5*level+CURR_SCORE;
        if (double_half == 'true') {
            NEW_SCORE = 2*NEW_SCORE;
        }
    } else {
        NEW_SCORE = CURR_SCORE;
        if (double_half == 'true') {
            NEW_SCORE = NEW_SCORE/2;
        }
    }
};

$(document).ready(function(e) {
    // TIMER HANDLER. ACTIVATE TIMER ON CLICK, IF NOT ALREADY TICKING.
    $(".card-header .card-timer").click(function() {
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

    // TEXT-BOX TYPING HANDLER
    $(".card-input .content").on('click', function() {
        // DISABLE INPUT IF CARD IS LOCKED, ELSE ENABLE IT
        if ($(".card-lock").find(".fa-lock").length) {
            $(this).attr("readonly","readonly");
        } else {
            if ($(this).attr("readonly") == "readonly")
                $(this).removeAttr("readonly");
        }

        // IF CARD IS UNLOCKED APPLY NEUTRAL ANSWER ON CLICK
        if ($(".card-lock").find(".fa-unlock").length) {
            $(".card-input .content").removeClass('wrong_answer');      // FOR DOUBLE TAKE CASE
            $(this).addClass('border_effect neutral_answer');
        }
    });

    // ENVOLOPE CLICK HANDLER
    $(".card-header .card-utils .fa-envelope-o").click(function() {
        var answer = $(".insights .ANS_OPT").attr("secanswer");
        // ONLY IF ITS NOT ALREADY RIGHT AND CARD-LOCK IS CLOSED
        if (!$("#option_"+answer+".option button").hasClass('right_answer') && $(".card-lock").find(".fa-lock").length) {
            // FOR TYPE 1
            $("#option_"+answer+".option button").addClass('right_answer');
            // FOR TYPE 2
            $(".card-input .content").removeClass('wrong_answer');
            $(".card-input .content").addClass('right_answer');
            $(".card-input .content").val(answer);
        }
    });

    // NEXT PAGE CLICK HANDLER BY POSTING DATA
    // (HIGHLY DANGEROUS AS ITS ASSUMES REQUEST DATA IS COMPLETED IN THOSE 2 SEC BEFORE 'animsition' DURATION ENDS)
    $(".card-header .card-utils .fa-arrow-right").on('click', function() {
        url = $(".insights .AJAXPOST_URL").attr("url");
        data = {
            'NEW_SCORE':NEW_SCORE,
            'LPAT':LPAT
        }
        // AFTER UPDATING POST REQUEST OF SCORE DATA, DO A GET REQUEST TO BRING IN NEW PAGE.
        $.ajax({
                type : "POST",
                url : url,
                data : data,
                success : function(data, status, xhr) {
                    console.log('POST UPDATE:'+data);
                    //window.location.href = url;
                },
                error: function(xhr, status, err) {
                    alert("XHR: "+xhr+" STATTUS: "+status+" ERR: "+err);
                },
                timeout:600
            });
    });

    // BEGINNING LIFELINE STATUS UPDATE
    LPAT = $(".insights .LPAT").attr("pattern");
    CURR_SCORE = parseInt($(".insights .CURR_SCORE").attr("score"));
    NEW_SCORE = CURR_SCORE  // NEW_SCORE is never used directly. But if left uninitialized, leads to undefined.
    if (LPAT[0] == "0")
        $(".card-header .card-lifelines .fa-mortar-board").addClass('card-lifeline-disable');
    if (LPAT[1] == "0")
        $(".card-header .card-lifelines .fa-smile-o").addClass('card-lifeline-disable');
    if (LPAT[2] == "0")
        $(".card-header .card-lifelines .fa-subscript").addClass('card-lifeline-disable');
    if (LPAT[3] == "0" || CURR_SCORE < 75)
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
