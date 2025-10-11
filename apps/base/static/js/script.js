(function () {
    const storageKey = 'theme-preference';
    const root = document.documentElement;
    const mediaQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

    const resolveTheme = (mode) => {
        if (mode === 'dark' || mode === 'light') {
            return mode;
        }
        if (mediaQuery) {
            return mediaQuery.matches ? 'dark' : 'light';
        }
        return 'light';
    };

    const applyTheme = (mode, persist) => {
        const resolved = resolveTheme(mode);
        root.dataset.themeMode = mode;
        root.dataset.theme = resolved;
        if (persist) {
            try {
                localStorage.setItem(storageKey, mode);
            } catch (error) {
                // LocalStorage isn't available (private mode or denied); ignore.
            }
        }
        updateButtons(mode);
    };

    const updateButtons = (mode) => {
        const buttons = document.querySelectorAll('.theme-toggle-btn[data-theme-value]');
        if (!buttons.length) {
            return;
        }
        buttons.forEach((button) => {
            button.classList.toggle('is-active', button.dataset.themeValue === mode);
        });
    };

    const handleButtonClick = (event) => {
        const button = event.currentTarget;
        const mode = button.dataset.themeValue;
        if (!mode) {
            return;
        }
        applyTheme(mode, true);
    };

    const init = () => {
        const storedMode = (() => {
            try {
                return localStorage.getItem(storageKey);
            } catch (error) {
                return null;
            }
        })();

        const initialMode = storedMode || root.dataset.themeMode || 'auto';
        applyTheme(initialMode, false);

        const buttons = document.querySelectorAll('.theme-toggle-btn[data-theme-value]');
        buttons.forEach((button) => {
            button.addEventListener('click', handleButtonClick);
        });

        if (mediaQuery) {
            const listener = () => {
                const currentMode = root.dataset.themeMode || 'auto';
                if (currentMode === 'auto') {
                    applyTheme('auto', false);
                }
            };
            if (typeof mediaQuery.addEventListener === 'function') {
                mediaQuery.addEventListener('change', listener);
            } else if (typeof mediaQuery.addListener === 'function') {
                mediaQuery.addListener(listener);
            }
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
