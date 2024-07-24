document.addEventListener('DOMContentLoaded', function() {
    var languageSelector = document.getElementById('language-selector');

    languageSelector.addEventListener('change', function() {
        var selectedLanguage = this.value;
        var url = new URL(window.location.href);

        url.searchParams.set('language', selectedLanguage);
        window.location.href = url.toString();
    });
});