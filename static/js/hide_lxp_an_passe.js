// Fonction permettant de cacher les champs inutiles du resp2
function Hide() {
    if(document.getElementById('ancien').checked) {
        $("#id_2-niveau_an_passe").prop("disabled", false);
        $("#id_2-gb_an_passe").prop("disabled", false);
        $("#id_2-ecco_an_passe").prop("disabled", false);
        $("#id_2-date_entretien").prop("disabled", true);
        $("#id_2-mee_entretien").prop("disabled", true);

    } else {
        $("#id_2-niveau_an_passe").prop("disabled", true);
        $("#id_2-gb_an_passe").prop("disabled", true);
        $("#id_2-ecco_an_passe").prop("disabled", true);
        $("#id_2-date_entretien").prop("disabled", false);
        $("#id_2-mee_entretien").prop("disabled", false);
    }
}
// Vérifie id_1-resp2 est à aucun (fonction Hide) après le chargement du document.
// Utile lors du retour en arrière dans le formulaire
document.addEventListener("DOMContentLoaded", function() {
    Hide();
});
// Appelle la fonction quand on change le statut de resp2
window.onload = function() {
    document.getElementById('ancien').onchange = Hide;
};