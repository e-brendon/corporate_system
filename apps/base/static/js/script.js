(function () {
    const storageKey = 'theme-preference';
    const root = document.documentElement;
    const mediaQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
    const autoResizeSelector = 'textarea[data-autoresize]';

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

    const getMinHeight = (textarea) => {
        const datasetValue = textarea.dataset.minHeight;
        if (datasetValue) {
            if (datasetValue.endsWith('rem')) {
                const remValue = parseFloat(datasetValue);
                if (!Number.isNaN(remValue)) {
                    return remValue * parseFloat(getComputedStyle(document.documentElement).fontSize || 16);
                }
            }
            if (datasetValue.endsWith('px')) {
                const pxValue = parseFloat(datasetValue);
                if (!Number.isNaN(pxValue)) {
                    return pxValue;
                }
            }
        }
        const styleValue = parseFloat(getComputedStyle(textarea).getPropertyValue('min-height'));
        return Number.isNaN(styleValue) ? 0 : styleValue;
    };

    const initAutoResize = () => {
        const textareas = document.querySelectorAll(autoResizeSelector);
        if (!textareas.length) {
            return;
        }
        textareas.forEach((textarea) => {
            const minHeight = getMinHeight(textarea);
            const resize = () => {
                textarea.style.height = 'auto';
                const newHeight = Math.max(textarea.scrollHeight, minHeight);
                textarea.style.height = `${newHeight}px`;
            };
            textarea.addEventListener('input', resize);
            // Adjust height on initialization (handles pre-filled values).
            resize();
        });
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

        initAutoResize();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
