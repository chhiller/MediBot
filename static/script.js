$(document).ready(function() {
    // Event listener for the speech button
    $("#speechButton").click(function() {
        // Initialize SpeechRecognition
        let recognition = new webkitSpeechRecognition() || new SpeechRecognition();
        recognition.lang = 'en-US';

        // Start speech recognition
        recognition.start();

        // Handle recognition result
        recognition.onresult = function(event) {
            let transcript = event.results[0][0].transcript;

            // Display transcript in the chat window
            let transcriptHtml = '<div class="bubbleWrapper"><div class="inlineContainer own"><div class="ownBubble own">' + transcript + '</div></div><span class="own"></span></div>';
            $("#chat").append(transcriptHtml);

            // Create button for sending the spoken text as a chat bubble
            let sendButtonHtml = '<button class="btn btn-primary mt-2 sendButton">Send</button>';
            $("#chat").append(sendButtonHtml);

            // Event listener for the send button
            $(".sendButton").click(function() {
                // Send transcript to server
                $.ajax({
                    type: "POST",
                    url: "/get",
                    data: {
                        'data': transcript
                    }
                }).done(function(data) {
                    // Display chatbot response
                    let botHtml = '<div class="bubbleWrapper"><div class="inlineContainer"><div class="otherBubble other">' + data + '</div></div><span class="other"></span></div>';
                    $("#chat").append(botHtml);
                });

                // Remove send button after sending the message
                $(this).remove();
            });
        };
    });
});
