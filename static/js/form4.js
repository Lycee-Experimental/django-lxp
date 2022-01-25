// Fonction permettant de cacher les champs inutiles du resp2
function Hide() {
    const value = document.getElementById('id_3-niveau').value;
    if(value === "deter" | value === "crepa") {
            document.getElementById('champ-spe').style.display = 'none';
        } else {
            document.getElementById('champ-spe').style.display = '';

        }
}
// Vérifie id_1-resp2 est à aucun (fonction Hide) après le chargement du document.
// Utile lors du retour en arrière dans le formulaire
document.addEventListener("DOMContentLoaded", Hide);
// Appelle la fonction quand on change le statut de resp2
window.onload = function() {
    document.getElementById('id_3-niveau').onchange = Hide;
};