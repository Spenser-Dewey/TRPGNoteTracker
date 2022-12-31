function showPopup(popupId) {
  console.log('WTF');
  console.log(popupId);
  const popup = document.getElementById(popupId);
  popup.classList.remove('hidden');
  return;
}

function hidePopup(popupId) {
  const popup = document.getElementById(popupId);
  popup.classList.add('hidden');
  return;
}