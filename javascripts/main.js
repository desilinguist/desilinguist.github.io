(function () {
    'use strict';

    // --- Section switching: works for both the SVG tree (desktop) and
    // --- the compact text nav (small screens) ---
    var currentId = 'firstchild';

    function selectBranch(childId) {
        if (childId === currentId) {
            return;
        }

        document.querySelector('.' + currentId + 'box').classList.remove('box-visible');
        document.querySelector('.' + childId + 'box').classList.add('box-visible');

        // keep the active state in sync across both navs
        document.querySelectorAll('#navtree g.active, #navtree-compact a.active').forEach(function (el) {
            el.classList.remove('active');
        });
        var branch = document.getElementById(childId);
        if (branch) {
            branch.classList.add('active');
        }
        var link = document.querySelector('#navtree-compact a[data-branch="' + childId + '"]');
        if (link) {
            link.classList.add('active');
        }

        // make sure the newly shown box is scrolled to the very top
        var content = document.querySelector('.' + childId + 'box .boxcontent');
        if (content) {
            content.scrollTop = 0;
        }

        currentId = childId;
    }

    document.querySelectorAll('#navtree g[id$="child"]').forEach(function (branch) {
        branch.addEventListener('click', function () {
            selectBranch(branch.id);
        });
    });

    document.querySelectorAll('#navtree-compact a').forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            selectBranch(link.getAttribute('data-branch'));
        });
    });

    // --- Dark mode toggle (choice persists in localStorage) ---
    var toggle = document.getElementById('theme-toggle');
    toggle.addEventListener('click', function () {
        var current = document.documentElement.getAttribute('data-theme');
        var next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    });

    // --- Name pronunciation: play in-page with howler.js, which handles
    // --- Safari's audio playback quirks (AudioContext unlocking etc.).
    // --- Falls back to the standalone page if playback fails. ---
    var pronounceLink = document.getElementById('pronounce-link');

    if (window.Howl) {
        var pronunciation = new Howl({
            src: ['name.mp3'],
            onplay: function () {
                pronounceLink.classList.add('playing');
            },
            onend: function () {
                pronounceLink.classList.remove('playing');
            },
            onloaderror: function () {
                fallbackToPronunciationPage();
            },
            onplayerror: function () {
                fallbackToPronunciationPage();
            }
        });

        pronounceLink.addEventListener('click', function (event) {
            event.preventDefault();
            pronunciation.play();
        });
    }

    function fallbackToPronunciationPage() {
        window.location.href = pronounceLink.href;
    }
})();
