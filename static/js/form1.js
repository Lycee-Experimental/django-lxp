// Fonction permettant de cacher les champs inutiles du resp2
function Hide() {

    if(!document.getElementById('select2-id_0-pays_naissance-container')) {
        setTimeout(Hide, 500);
    }
    else {
        if(document.getElementById('select2-id_0-pays_naissance-container').textContent === "FRANCE") {
            document.getElementById('div_id_0-depCOM_naissance').style.display = '';
            document.getElementById('div_id_0-commune_naissance').style.display = '';
            document.getElementById('div_id_0-ville_naissance_etrangere').style.display = 'none';
        } else {
            document.getElementById('div_id_0-depCOM_naissance').style.display = 'none';
            document.getElementById('div_id_0-commune_naissance').style.display = 'none';
            document.getElementById('div_id_0-ville_naissance_etrangere').style.display = '';
        }
    }

}

// Vérifie id_1-resp2 est à aucun (fonction Hide) après le chargement du document.
// Utile lors du retour en arrière dans le formulaire
document.addEventListener("DOMContentLoaded", Hide);
// Appelle la fonction quand on change le statut de resp2
window.onload = function() {
    document.getElementById('id_0-pays_naissance').onchange = Hide;
};