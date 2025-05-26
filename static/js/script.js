document.addEventListener('DOMContentLoaded', function() {
    const output = document.getElementById('output');
    const suggestionsDiv = document.getElementById('suggestions');
    const keySound = document.getElementById('keySound');
    
    let currentSequence = [];
    let pressedKeys = new Set();
    let currentWord = '';
    let userId = 'user_' + Math.random().toString(36).substr(2, 9);
    
    // Track key presses
    document.addEventListener('keydown', function(e) {
        // Only process Braille keys (d, w, q, k, o, p) and control keys
        const validKeys = ['d', 'w', 'q', 'k', 'o', 'p', ' ', 'Backspace', 'Enter'];
        
        if (!validKeys.includes(e.key)) return;
        
        e.preventDefault();
        
        // Play key sound
        keySound.currentTime = 0;
        keySound.play();
        
        // Handle control keys
        if (e.key === ' ') {
            finishWord();
            output.textContent += ' ';
            currentWord = '';
            return;
        } else if (e.key === 'Backspace') {
            if (currentSequence.length > 0) {
                currentSequence.pop();
                updateOutput();
            } else if (output.textContent.length > 0) {
                output.textContent = output.textContent.slice(0, -1);
                currentWord = currentWord.slice(0, -1);
            }
            return;
        } else if (e.key === 'Enter') {
            finishWord();
            output.textContent += '\n';
            currentWord = '';
            return;
        }
        
        // Add to pressed keys
        if (!pressedKeys.has(e.key)) {
            pressedKeys.add(e.key);
            updateCurrentSequence();
        }
    });
    
    document.addEventListener('keyup', function(e) {
        if (pressedKeys.has(e.key)) {
            pressedKeys.delete(e.key);
            
            // If no keys are pressed, send the sequence
            if (pressedKeys.size === 0 && currentSequence.length > 0) {
                sendSequenceToServer();
            }
        }
    });
    
    function updateCurrentSequence() {
        currentSequence = Array.from(pressedKeys).sort();
        updateOutput();
    }
    
    function updateOutput() {
        // Show the current sequence as placeholder
        const displayText = output.textContent.replace(/\?$/, '');
        output.textContent = displayText + (currentSequence.length > 0 ? '?' : '');
    }
    
    function sendSequenceToServer() {
    const sequence = currentSequence.join('');
    
    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sequence: sequence,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.char && data.char !== '?') {
            // Visual feedback for corrected characters
            const charSpan = document.createElement('span');
            charSpan.textContent = data.char;
            
            if (data.was_corrected) {
                charSpan.className = 'corrected-char';
                setTimeout(() => {
                    charSpan.className = '';
                }, 1000);
            }
            
            // Replace the placeholder '?' with the character
            const outputText = output.textContent.replace(/\?$/, '');
            output.textContent = outputText;
            output.appendChild(charSpan);
            
            currentWord += data.char;
            currentSequence = [];
            
            // Get suggestions as we type
            if (currentWord.length > 0) {
                getSuggestions(currentWord);
            }
        }
    });
}
    
    function finishWord() {
        if (currentWord.length > 0) {
            getSuggestions(currentWord, true);
        }
    }
    
    function getSuggestions(word, isFinal = false) {
        fetch('/suggest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                word: word,
                user_id: userId
            })
        })
        .then(response => response.json())
        .then(data => {
            showSuggestions(data.suggestions, isFinal);
        });
    }
    
    function showSuggestions(suggestions, isFinal) {
        suggestionsDiv.innerHTML = '';
        
        if (suggestions.length === 0) return;
        
        suggestions.forEach(suggestion => {
            const suggestionEl = document.createElement('div');
            suggestionEl.className = 'suggestion';
            suggestionEl.textContent = suggestion;
            
            suggestionEl.addEventListener('click', () => {
                // Replace current word with suggestion
                const text = output.textContent;
                const lastSpace = text.lastIndexOf(' ');
                const newText = lastSpace === -1 ? 
                    suggestion : 
                    text.substring(0, lastSpace + 1) + suggestion;
                
                output.textContent = newText;
                currentWord = suggestion;
                suggestionsDiv.innerHTML = '';
                
                // Send correction to server for learning
                if (isFinal) {
                    sendCorrectionToServer(text.substring(lastSpace + 1), suggestion);
                }
            });
            
            suggestionsDiv.appendChild(suggestionEl);
        });
    }
    
    function sendCorrectionToServer(original, corrected) {
        fetch('/learn', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                original: original,
                corrected: corrected,
                user_id: userId
            })
        });
    }
});