const express = require('express');
const app = express();

// Serve static files (HTML, CSS, JS)
app.use(express.static('public')); 

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html'); 
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
