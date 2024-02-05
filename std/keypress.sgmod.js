const chackablekeyboardCharacters = [
    // Alphabets: A-Z, a-z
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    // Numbers: 0-9
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    // Special characters
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=',
    '+', '[', '{', ']', '}', '\\', '|', ';', ':', "'", '"', ',', '<',
    '.', '>', '/', '?', '`',
    // Space and control characters
    ' ', 'Tab', 'Backspace', 'Enter', 'Shift', 'Control', 'Alt', 'CapsLock',
    // Arrow keys
    'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
    // Function keys
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
    // Other common keys
    'Escape', 'Insert', 'Delete', 'Home', 'End', 'PageUp', 'PageDown'
];
const chackablekeyboardCharactersvalue = {};
chackablekeyboardCharacters.forEach(char => {
    chackablekeyboardCharactersvalue[char] = 0
})

function keyPressed(s){
    if (chackablekeyboardCharacters.includes(s)) {
        return chackablekeyboardCharactersvalue[s] ? 1 : 0;
    }
}

function getPressedKeys(){
    ret = []
    chackablekeyboardCharacters.forEach(char =>{
        if (chackablekeyboardCharactersvalue[char] == 1){
            ret.push(char)
        }
    })
    return ret
}

window.addEventListener("keydown", (e)=> {
    chackablekeyboardCharactersvalue[e.key] = 1
}, false)

window.addEventListener("keyup", (e)=> {
    chackablekeyboardCharactersvalue[e.key] = 0
}, false)