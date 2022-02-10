// Fonction permettant de cacher les champs inutiles du resp2
function Hide() {
    if(document.getElementById('nouvelle').checked) {
    document.getElementById('div_id_2-niveau_an_passe').style.display = 'none';
    document.getElementById('div_id_2-gb_an_passe').style.display = 'none';
    document.getElementById('div_id_2-ecco_an_passe').style.display = 'none';
    } else {
        document.getElementById('div_id_2-niveau_an_passe').style.display = '';
        document.getElementById('div_id_2-gb_an_passe').style.display = '';
        document.getElementById('div_id_2-ecco_an_passe').style.display = '';
    }
}
// Vérifie id_1-resp2 est à aucun (fonction Hide) après le chargement du document.
// Utile lors du retour en arrière dans le formulaire
document.addEventListener("DOMContentLoaded", function() {
    Hide();
});
// Appelle la fonction quand on change le statut de resp2
window.onload = function() {
    document.getElementById('nouvelle').onchange = Hide;
};