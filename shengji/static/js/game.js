$(function() {
    var scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
    var socket = new ReconnectingWebSocket(scheme + '://' + window.location.host + '/game' + window.location.pathname);

    class Player extends React.Component {
        constructor(props) {
          super(props);
          this.getReady = this.getReady.bind(this);
          this.switchPlayer = this.switchPlayer.bind(this);
        }

        getReady(e) {
            e.preventDefault();
            var payload = {
                command: 'get_ready',
            }
            socket.send(JSON.stringify(payload));
            e.target.blur();
        }

        switchPlayer(e) {
            e.preventDefault();
            var payload = {
                command: 'switch_player',
                from_player_order: this.props.fromPlayerOrder,
                to_player_order: this.props.toPlayerOrder,
            }
            socket.send(JSON.stringify(payload));
            e.target.blur();
        }

        render() {
            var button;
            if (this.props.playerPos === 'bottom-player') {
                button = <button className="btn btn-link" onClick={this.getReady}>Start</button>;
            } else {
                button = <button className="btn btn-link" onClick={this.switchPlayer}>Switch</button>;
            }
            return (
                <div className="player" id={this.props.playerPos}>
                    <div>{this.props.username}</div>
                    {button}
                </div>
            );
        }
    }

    socket.onmessage = function(message) {
        var payload = JSON.parse(message.data);
        if (payload.command === 'request_player_list') {
            var newPayload = {
                command: 'update_player_list',
            }
            socket.send(JSON.stringify(newPayload));
        } else if (payload.command === 'new_player_list') {
            ReactDOM.render(
                <div>
                    <Player
                        playerPos="bottom-player"
                        fromPlayerOrder={payload.player_order_rotation_list[0]}
                        toPlayerOrder={payload.player_order_rotation_list[0]}
                        username={payload.username_list[0]}
                    />
                    <Player
                        playerPos="right-player"
                        fromPlayerOrder={payload.player_order_rotation_list[0]}
                        toPlayerOrder={payload.player_order_rotation_list[1]}
                        username={payload.username_list[1]}
                    />
                    <Player
                        playerPos="top-player"
                        fromPlayerOrder={payload.player_order_rotation_list[0]}
                        toPlayerOrder={payload.player_order_rotation_list[2]}
                        username={payload.username_list[2]}
                    />
                    <Player
                        playerPos="left-player"
                        fromPlayerOrder={payload.player_order_rotation_list[0]}
                        toPlayerOrder={payload.player_order_rotation_list[3]}
                        username={payload.username_list[3]}
                    />
                </div>,
                document.getElementById('table')
            );
        }
    };
});
