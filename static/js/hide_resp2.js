// Fonction permettant de cacher les champs inutiles du resp2
function Hide() {
    if(document.getElementById('id_1-resp2').options[document.getElementById('id_1-resp2').selectedIndex].value == "aucun") {
    document.getElementById('div_id_1-nom_resp2').style.display = 'none';
    document.getElementById('div_id_1-prenom_resp2').style.display = 'none';
    document.getElementById('div_id_1-adresse_resp2').style.display = 'none';
    document.getElementById('div_id_1-tel_resp2').style.display = 'none';
    document.getElementById('div_id_1-email_resp2').style.display = 'none';
    document.getElementById('div_id_1-sociopro_resp2').style.display = 'none';
    } else {
        document.getElementById('div_id_1-nom_resp2').style.display = '';
        document.getElementById('div_id_1-prenom_resp2').style.display = '';
        document.getElementById('div_id_1-adresse_resp2').style.display = '';
        document.getElementById('div_id_1-tel_resp2').style.display = '';
        document.getElementById('div_id_1-email_resp2').style.display = '';
        document.getElementById('div_id_1-sociopro_resp2').style.display = '';
    }
}
// Vérifie id_1-resp2 est à aucun (fonction Hide) après le chargement du document.
// Utile lors du retour en arrière dans le formulaire
document.addEventListener("DOMContentLoaded", function() {
    Hide();
});
// Appelle la fonction quand on change le statut de resp2
window.onload = function() {
    document.getElementById('id_1-resp2').onchange = Hide;
};