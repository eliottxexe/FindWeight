// Fonction pour afficher un message de bienvenue lorsque la page est entièrement chargée
document.addEventListener('DOMContentLoaded', function() {
    console.log('La page est entièrement chargée.');
    alert('Bienvenue sur le site de téléchargement !');
});

// Fonction pour suivre les clics sur le bouton de téléchargement
const downloadButton = document.querySelector('.download-button');

downloadButton.addEventListener('click', function(event) {
    console.log('Clic sur le bouton de téléchargement.');
    // Vous pouvez ajouter d'autres actions ici, comme le suivi d'événements ou l'affichage de messages
});
