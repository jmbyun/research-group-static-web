function handleScroll() {
    window.__store__ = window.__store__ || {};
    var top = window.scrollY;
    var threshold = 30;
    if (!window.__store__.scrolled && top > threshold) {
        window.__store__.scrolled = true;
        document.getElementById('header').className = 'header header-scrolled';
    } else if (window.__store__.scrolled && top <= threshold) {
        window.__store__.scrolled = false;
        document.getElementById('header').className = 'header';
    }
}
window.addEventListener('scroll', handleScroll);
