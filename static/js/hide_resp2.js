// Fonction permettant de cacher les champs inutiles du resp2
function Hide() {
    if(document.getElementById('id_1-resp2').options[document.getElementById('id_1-resp2').selectedIndex].value == "aucun") {
        $("#id_1-nom_resp2").prop("disabled", true);
        $("#id_1-civilite_resp2").prop("disabled", true);
        $("#id_1-prenom_resp2").prop("disabled", true);
        $("#id_1-adresse_resp2").prop("disabled", true);
        $("#id_1-tel_resp2").prop("disabled", true);
        $("#id_1-email_resp2").prop("disabled", true);
        $("#id_1-sociopro_resp2").prop("disabled", true);
    } else {
        $("#id_1-nom_resp2").prop("disabled", false);
        $("#id_1-civilite_resp2").prop("disabled", false);
        $("#id_1-prenom_resp2").prop("disabled", false);
        $("#id_1-adresse_resp2").prop("disabled", false);
        $("#id_1-tel_resp2").prop("disabled", false);
        $("#id_1-email_resp2").prop("disabled", false);
        $("#id_1-sociopro_resp2").prop("disabled", false);
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