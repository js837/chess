var Tree = function(fen, colour, score, from, to) {
    var self = this;
    this.fen = ko.observable(fen);
    this.position = new ChessPosition(fen, null, [], colour, score, from, to)
    this.score = ko.observable(score)
    this.colour = ko.observable(colour)
    this.showPosition = ko.observable(false);
    this.toggleShowPosition = function () { self.showPosition(!self.showPosition()) };
    this.moves = ko.observableArray([]);
    this.showChildren = ko.observable(false)

    this.toggleShowChildren = function(){
        // Going from 'hidden' to 'show' so populate moves observable
        if (!self.showChildren() && !self.moves().length){
            self.getAvailableMoves()
        }
        this.showChildren(!this.showChildren())
    }

    this.getAvailableMoves = function(){
         $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({fen:self.fen(), ai:false}),
            dataType: 'json',
            url: '/get-moves'
        }).done(function(newPosition){
            $.each(newPosition.moves, function(i, move){
                self.moves.push(new Tree(move.fen, move.colour, move.score, move.from, move.to))
            })
        })
    }
}


var App = function(){
    var self = this
    globalApp = this
    var startingPosition = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                            "result": null,
                            "score": 0,
                            "colour": true,
                            "from": null,
                            "to": null,
                            "moves": [{"fen": "rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq - 1 1", "from": [0, 1], "newPiece": null, "to": [2, 2]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b KQkq - 1 1", "from": [0, 1], "newPiece": null, "to": [2, 0]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/7N/PPPPPPPP/RNBQKB1R b KQkq - 1 1", "from": [0, 6], "newPiece": null, "to": [2, 7]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1", "from": [0, 6], "newPiece": null, "to": [2, 5]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq - 0 1", "from": [1, 0], "newPiece": null, "to": [2, 0]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1", "from": [1, 0], "newPiece": null, "to": [3, 0]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq - 0 1", "from": [1, 1], "newPiece": null, "to": [2, 1]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR b KQkq b3 0 1", "from": [1, 1], "newPiece": null, "to": [3, 1]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq - 0 1", "from": [1, 2], "newPiece": null, "to": [2, 2]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq c3 0 1", "from": [1, 2], "newPiece": null, "to": [3, 2]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1", "from": [1, 3], "newPiece": null, "to": [2, 3]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1", "from": [1, 3], "newPiece": null, "to": [3, 3]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b KQkq - 0 1", "from": [1, 4], "newPiece": null, "to": [2, 4]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", "from": [1, 4], "newPiece": null, "to": [3, 4]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/5P2/PPPPP1PP/RNBQKBNR b KQkq - 0 1", "from": [1, 5], "newPiece": null, "to": [2, 5]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR b KQkq f3 0 1", "from": [1, 5], "newPiece": null, "to": [3, 5]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR b KQkq - 0 1", "from": [1, 6], "newPiece": null, "to": [2, 6]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR b KQkq g3 0 1", "from": [1, 6], "newPiece": null, "to": [3, 6]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/8/7P/PPPPPPP1/RNBQKBNR b KQkq - 0 1", "from": [1, 7], "newPiece": null, "to": [2, 7]},
                                      {"fen": "rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPP1/RNBQKBNR b KQkq h3 0 1", "from": [1, 7], "newPiece": null, "to": [3, 7]}
                            ]}


    self.mainBoard = new ChessPosition(
        startingPosition.fen,
        startingPosition.result,
        startingPosition.moves,
        startingPosition.colour,
        startingPosition.score,
        startingPosition.from,
        startingPosition.to
    )

    // Start a new game on load
    this.newGame = function(){
        self.mainBoard.fen(startingPosition.fen)
        self.mainBoard.result(startingPosition.result)
        self.mainBoard.moves(startingPosition.moves)
    }

    this.tree = ko.pureComputed(function(){
        return new Tree(self.mainBoard.fen(), self.mainBoard.colour(), self.mainBoard.score(), self.mainBoard.from(), self.mainBoard.to());
    })



}



var ChessPosition = function(fen, result, moves, colour, score, from, to) {
    var position = this;
    var chessChars = {
        K : {W: '&#9812;', B: '&#9818;'},
        Q : {W: '&#9813;', B: '&#9819;'},
        B : {W: '&#9815;', B: '&#9821;'},
        N : {W: '&#9816;', B: '&#9822;'},
        R : {W: '&#9814;', B: '&#9820;'},
        P : {W: '&#9817;', B: '&#9823;'},
    }

    var Square = function(coord, pieceHtml){
        var self = this;
        this.coord = coord;
        this.pieceHtml = pieceHtml || '&nbsp;';
        this.hightlight = ko.pureComputed(function(){
            var selected_bool = $.grep(position.getAvailableMoves(), function(move){
                return move.to[0] === self.coord[0] && move.to[1] === self.coord[1]
            }).length
            if (position.to() && position.from()) {
                var move_from_bool = position.from()[0] === self.coord[0] && position.from()[1] === self.coord[1]
                var move_to_bool = position.to()[0] === self.coord[0] && position.to()[1] === self.coord[1]
            }
            return selected_bool || move_from_bool || move_to_bool
        })

        this.selectSquare = function(){
            var self = this;
            var moveGrep = $.grep(position.getAvailableMoves(), function(move){
                return move.to[0] === self.coord[0] && move.to[1] === self.coord[1]
            })
            if (moveGrep.length){
                position.startCoord([null, null])
                // End move
                var move = moveGrep[0]
                position.fen(move.fen)

                 $.ajax({
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({fen:move.fen,ai:true}),
                    dataType: 'json',
                    url: '/get-moves'
                }).done(function(newPosition){
                    position.fen(newPosition.new_fen)
                    position.refreshBoard(newPosition)
                })



            } else{
                // Start move
                position.startCoord(this.coord)
            }
        }
    }


    this.bestMoveFen = ko.observable()

//    this.getBestMove = function(move){
//         $.ajax({
//            type: 'POST',
//            contentType: 'application/json',
//            data: JSON.stringify({fen:move.fen,ai:true}),
//            dataType: 'json',
//            url: '/get-moves'
//        }).done(function(newPosition){
//            position.bestMoveFen(newPosition.new_fen)
//            position.refreshBoard(newPosition)
//        })
//    }





    this.fen = ko.observable(fen);
    this.result = ko.observable(result);
    this.moves = ko.observable(moves || [])
    this.colour = ko.observable(colour)
    this.score = ko.observable(score)
    this.from = ko.observable(from)
    this.to = ko.observable(to)

    this.startCoord = ko.observable([null,null])

    this.getAvailableMoves = function(){
        return $.grep(position.moves(), function(move){
            return move.from[0] === position.startCoord()[0] && move.from[1] === position.startCoord()[1]
        })
    }


    this.refreshBoard = function(newPosition){
        position.result(newPosition.result)
        position.moves(newPosition.moves)
        position.colour(newPosition.colour)
        position.score(newPosition.score)
        position.from(newPosition.from)
        position.to(newPosition.to)
    }

//    this.fen.subscribe(function(newFen){
//         $.ajax({
//            type: 'POST',
//            contentType: 'application/json',
//            data: JSON.stringify({fen:newFen,ai:false}),
//            dataType: 'json',
//            url: '/get-moves'
//        }).done(function(newPosition){
//            position.refreshBoard(newPosition)
//        })
//    })


    this.board = ko.pureComputed(function(){
        // Separate the 6 components
        var fen_components = position.fen().trim().split(' ')
        var board_str = fen_components[0]
        
        // Construct the board
        var board = []
        var rank_list = board_str.split('/')

        for (var i=0; i< rank_list.length; i++){
            var rank_str = rank_list[i]
            var rank = []
            var l = 0;
            for (var j=0; j<rank_str.length; j++){
                var piece_str = rank_str[j]
                if (['1','2','3','4','5','6','7','8'].indexOf(piece_str) != -1) {
                    // Add blanks squares
                    var blanks = []
                    for (var k=0; k<parseInt(piece_str); k++){
                        blanks.push(new Square([7-i, l++]));
                    }
                    rank = rank.concat(blanks)
                } else {
                    // Add pieces
                    var piece_colour = (piece_str == piece_str.toUpperCase()) ? 'W' : 'B'
                    var pieceHtml = chessChars[piece_str.toUpperCase()][piece_colour]
                    rank.push(new Square([7-i,l++], pieceHtml))
                }
            }
            board.push(rank)
        }   
        return board
    })




}






ko.applyBindings(new App());