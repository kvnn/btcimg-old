(function(){

    function satoshiToBitcoin(num_satoshi) {
        return 0.00000001 * num_satoshi;
    }

    function updateBtcLeft(btcContribution) {
        var current = parseFloat($('#btcLeft').text());
        var updated = current - btcContribution;
        $('#btcLeft').text(updated);
    }

    function handleTx(response, assetAddress) {
        var amount = 0;
            
        for(var i=0;i<response.x.out.length;i++) {
            if (response.x.out[i].addr == assetAddress) {
                amount += response.x.out[i].value;
            }
        }

        amount = satoshiToBitcoin(amount);

        if (amount <= 0) {
            window.location.reload();
        } else {
            updateBtcLeft(amount);
        }
    }


    $(function(){ // on load
        var connection = new WebSocket('ws://ws.blockchain.info/inv'),
            assetAddress = $('#asset').data('address');

        connection.onopen = function() {
            
            connection.send(JSON.stringify({"op":"addr_sub", "addr": assetAddress}));
            // connection.send( JSON.stringify( {"op":"unconfirmed_sub"} ) );  //  subscribe to uncofirmed activity
            // connection.send( JSON.stringify( {"op":"blocks_sub"} ) );       //  subscribe to new blocks
        };

        connection.onerror = function(error) {
            // console.log('Address connection error:', error);
        };

        connection.onmessage = function(msg) {
            var response = JSON.parse(msg.data);

            // New transaction
            if (response.op == "utx") handleTx(response, assetAddress);

        };

        window.connection = connection;
    });
})();