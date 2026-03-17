// Chinese Simplified/Traditional Conversion using OpenCC-js
// Uses OpenCC for accurate conversion (no variant/archaic character issues)

var zh_default = 'n';
var zh_choose = 'n';

var _s2tConverter = null;
var _t2sConverter = null;

function _getS2TConverter() {
    if (!_s2tConverter && typeof OpenCC !== 'undefined') {
        _s2tConverter = OpenCC.Converter({ from: 'cn', to: 'tw' });
    }
    return _s2tConverter;
}

function _getT2SConverter() {
    if (!_t2sConverter && typeof OpenCC !== 'undefined') {
        _t2sConverter = OpenCC.Converter({ from: 'tw', to: 'cn' });
    }
    return _t2sConverter;
}

// Store original text for accurate back-conversion
var _originalTexts = new WeakMap();

function zh_tran(go) {
    if (go) zh_choose = go;
    localStorage.setItem('zh_choose', zh_choose);

    if (go == 'n') return;

    if (typeof OpenCC === 'undefined') {
        console.warn('OpenCC library not loaded, cannot perform conversion');
        return;
    }

    handleNode(document.body);
}

function handleNode(node) {
    var childs = node.childNodes;
    for (var i = 0; i < childs.length; i++) {
        var n = childs[i];
        if (n.nodeType == 3) { // Text node
            // Store original simplified text on first conversion
            if (!_originalTexts.has(n)) {
                _originalTexts.set(n, n.data);
            }
            if (zh_choose == 't') {
                // Always convert from original simplified to traditional
                var converter = _getS2TConverter();
                if (converter) {
                    n.data = converter(_originalTexts.get(n));
                }
            } else if (zh_choose == 's') {
                // Restore original simplified text
                n.data = _originalTexts.get(n);
            }
        } else if (n.nodeType == 1) { // Element node
            if (['SCRIPT', 'STYLE', 'CODE', 'PRE'].indexOf(n.tagName) == -1) {
                handleNode(n);
            }
            if (n.tagName == 'INPUT' || n.tagName == 'TEXTAREA') {
                if (n.placeholder) {
                    n.placeholder = translateText(n.placeholder);
                }
                if (n.value && ['button', 'submit', 'reset'].indexOf(n.type) > -1) {
                    n.value = translateText(n.value);
                }
            }
            if (n.title) {
                n.title = translateText(n.title);
            }
        }
    }
}

function translateText(str) {
    if (str == "" || str == null) return "";
    if (zh_choose == 't') {
        var converter = _getS2TConverter();
        return converter ? converter(str) : str;
    } else if (zh_choose == 's') {
        var converter = _getT2SConverter();
        return converter ? converter(str) : str;
    }
    return str;
}
