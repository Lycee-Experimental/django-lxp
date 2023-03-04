// Fonction permettant de cacher les champs inutiles du resp2
function HideAncien() {
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
function HideDesco() {
    if(document.getElementById('desco').checked) {
        $("#id_2-etablissement_origine").prop("disabled", true);
    } else {
        $("#id_2-etablissement_origine").prop("disabled", false);
    }
}
// Vérifie id_1-resp2 est à aucun (fonction Hide) après le chargement du document.
// Utile lors du retour en arrière dans le formulaire
document.addEventListener("DOMContentLoaded", function() {
    HideAncien();
    HideDesco();
});
// Appelle la fonction quand on change le statut de resp2
window.onload = function() {
    document.getElementById('ancien').onchange = HideAncien;
    document.getElementById('desco').onchange = HideDesco;

};