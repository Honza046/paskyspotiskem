/**
 * Live 3D tape configurator (Three.js) — fullscreen modal.
 */
(function (global) {
    'use strict';

    var COLOR_MAP = {
        'bílá': 0xffffff,
        'hnědá': 0x9c663b,
        'transparentní': 0xffffff,
        'jiná': 0xffffff,
    };

    // 1 unit = 10 cm
    var BASE_WIDTH_MM = 50;
    var TAPE_OUTER_R = 1.2;
    var TAPE_INNER_R = 0.8;
    var TAPE_HEIGHT = 0.5;
    var TAPE_ROLL_TEXTURE_REPEAT = 5;
    var TAPE_ROUGHNESS = 0.1;
    var TAPE_METALNESS = 0;
    var TAPE_CLEARCOAT = 1.0;
    var TAPE_CLEARCOAT_ROUGHNESS = 0.05;
    var TAPE_TRANSPARENT_OPACITY = 0.4;

    var BOX_WIDTH = 3.0;
    var BOX_HEIGHT = 2.0;
    var BOX_DEPTH = 2.0;
    var BOX_CARDBOARD_COLOR = 0xc29b6f;
    var BOX_TAPE_DEPTH = 0.5;
    var BOX_TAPE_TEXTURE_REPEAT_U = 2.5;
    var BOX_SURFACE_OFFSET = 0.005;
    var BOX_CROSS_TAPE_TOP_Y = 1.01;
    var BOX_INTERSECTION_PATCH_Y = 1.015;
    var PATCH_CANVAS_SIZE = 512;

    var CARDBOARD_CORE_COLOR = 0xd4c4a8;
    var CANVAS_W = 1024;
    var CANVAS_H = 256;
    var FULL_CIRCLE = Math.PI * 2;

    function getBoxTapeTextureRepeat(widthMm) {
        var w = parseInt(widthMm, 10) || BASE_WIDTH_MM;
        var scale = w / BASE_WIDTH_MM;
        return {
            u: BOX_TAPE_TEXTURE_REPEAT_U,
            v: 1 / scale,
        };
    }

    function configureBoxTapeTexture(texture) {
        var THREE = global.THREE;
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.minFilter = THREE.LinearFilter;
        texture.magFilter = THREE.LinearFilter;
        texture.generateMipmaps = false;
        texture.anisotropy = 8;
        texture.center.set(0.5, 0.5);
        texture.rotation = Math.PI / 2;
    }

    function createBoxTapeMaterial(texture, colorKey) {
        var THREE = global.THREE;
        var isTransparent = colorKey === 'transparentní';
        var mat = createTapeMaterial(texture, colorKey);
        mat.side = THREE.DoubleSide;
        mat.transparent = isTransparent;
        mat.depthWrite = true;
        mat.opacity = isTransparent ? TAPE_TRANSPARENT_OPACITY : 1;
        return mat;
    }

    function createBoxTapePatchMaterial(texture, colorKey) {
        var THREE = global.THREE;
        var isTransparent = colorKey === 'transparentní';
        return new THREE.MeshPhysicalMaterial({
            map: texture,
            color: tapeMaterialColor(colorKey),
            roughness: TAPE_ROUGHNESS,
            metalness: TAPE_METALNESS,
            clearcoat: TAPE_CLEARCOAT,
            clearcoatRoughness: TAPE_CLEARCOAT_ROUGHNESS,
            side: THREE.DoubleSide,
            transparent: isTransparent,
            opacity: isTransparent ? TAPE_TRANSPARENT_OPACITY : 1,
            depthWrite: true,
        });
    }

    function applyBoxTapeMaterialState(material, colorKey) {
        var isTransparent = colorKey === 'transparentní';
        applyTapeMaterialState(material, colorKey);
        material.side = global.THREE.DoubleSide;
        material.transparent = isTransparent;
        material.depthWrite = true;
        material.opacity = isTransparent ? TAPE_TRANSPARENT_OPACITY : 1;
        material.needsUpdate = true;
    }

    function applyBoxTapePatchMaterialState(material, colorKey) {
        var isTransparent = colorKey === 'transparentní';
        material.color.setHex(tapeMaterialColor(colorKey));
        material.roughness = TAPE_ROUGHNESS;
        material.metalness = TAPE_METALNESS;
        material.clearcoat = TAPE_CLEARCOAT;
        material.clearcoatRoughness = TAPE_CLEARCOAT_ROUGHNESS;
        material.transparent = isTransparent;
        material.opacity = isTransparent ? TAPE_TRANSPARENT_OPACITY : 1;
        material.depthWrite = true;
        material.side = global.THREE.DoubleSide;
        material.needsUpdate = true;
    }

    function buildBoxIntersectionPatch(THREE, material, tapeWidth) {
        var patch = new THREE.Mesh(
            new THREE.PlaneGeometry(tapeWidth, tapeWidth),
            material
        );
        patch.rotation.x = -Math.PI / 2;
        patch.position.set(0, BOX_INTERSECTION_PATCH_Y, 0);
        patch.renderOrder = 3;
        return patch;
    }

    function resizeBoxIntersectionPatch(patch, tapeWidth) {
        var THREE = global.THREE;
        if (patch.geometry) patch.geometry.dispose();
        patch.geometry = new THREE.PlaneGeometry(tapeWidth, tapeWidth);
    }

    function buildBoxTapeGroup(THREE, material, tapeWidth) {
        var group = new THREE.Group();
        var topY = BOX_HEIGHT / 2 + BOX_SURFACE_OFFSET;
        var halfZ = BOX_DEPTH / 2 + BOX_SURFACE_OFFSET;

        var topTape = new THREE.Mesh(
            new THREE.PlaneGeometry(tapeWidth, BOX_DEPTH),
            material
        );
        topTape.rotation.x = -Math.PI / 2;
        topTape.position.set(0, topY, 0);
        topTape.renderOrder = 1;

        var frontTape = new THREE.Mesh(
            new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT),
            material
        );
        frontTape.position.set(0, 0, halfZ);
        frontTape.renderOrder = 1;

        var backTape = new THREE.Mesh(
            new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT),
            material
        );
        backTape.rotation.y = Math.PI;
        backTape.position.set(0, 0, -halfZ);
        backTape.renderOrder = 1;

        group.add(topTape, frontTape, backTape);

        return {
            group: group,
            topTape: topTape,
            frontTape: frontTape,
            backTape: backTape,
        };
    }

    function resizeBoxTapePlanes(tapes, tapeWidth) {
        var THREE = global.THREE;

        if (tapes.topTape.geometry) tapes.topTape.geometry.dispose();
        tapes.topTape.geometry = new THREE.PlaneGeometry(tapeWidth, BOX_DEPTH);

        if (tapes.frontTape.geometry) tapes.frontTape.geometry.dispose();
        tapes.frontTape.geometry = new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT);

        if (tapes.backTape.geometry) tapes.backTape.geometry.dispose();
        tapes.backTape.geometry = new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT);
    }

    function buildBoxCrossTapeGroup(THREE, material, tapeWidth) {
        var group = new THREE.Group();
        var halfX = BOX_WIDTH / 2 + BOX_SURFACE_OFFSET;

        var topTape = new THREE.Mesh(
            new THREE.PlaneGeometry(BOX_WIDTH, tapeWidth),
            material
        );
        topTape.rotation.x = -Math.PI / 2;
        topTape.position.set(0, BOX_CROSS_TAPE_TOP_Y, 0);
        topTape.renderOrder = 2;

        var leftTape = new THREE.Mesh(
            new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT),
            material
        );
        leftTape.rotation.y = -Math.PI / 2;
        leftTape.position.set(-halfX, 0, 0);
        leftTape.renderOrder = 1;

        var rightTape = new THREE.Mesh(
            new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT),
            material
        );
        rightTape.rotation.y = Math.PI / 2;
        rightTape.position.set(halfX, 0, 0);
        rightTape.renderOrder = 1;

        group.add(topTape, leftTape, rightTape);

        return {
            group: group,
            topTape: topTape,
            leftTape: leftTape,
            rightTape: rightTape,
        };
    }

    function resizeBoxCrossTapePlanes(tapes, tapeWidth) {
        var THREE = global.THREE;

        if (tapes.topTape.geometry) tapes.topTape.geometry.dispose();
        tapes.topTape.geometry = new THREE.PlaneGeometry(BOX_WIDTH, tapeWidth);

        if (tapes.leftTape.geometry) tapes.leftTape.geometry.dispose();
        tapes.leftTape.geometry = new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT);

        if (tapes.rightTape.geometry) tapes.rightTape.geometry.dispose();
        tapes.rightTape.geometry = new THREE.PlaneGeometry(tapeWidth, BOX_HEIGHT);
    }

    function createCardboardBumpTexture() {
        var THREE = global.THREE;
        var size = 256;
        var canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        var ctx = canvas.getContext('2d');
        var imageData = ctx.createImageData(size, size);
        var data = imageData.data;
        var x;
        var y;
        var i;

        for (y = 0; y < size; y++) {
            for (x = 0; x < size; x++) {
                var n = 0;
                var octave;
                var amp = 1;
                var freq = 1;
                for (octave = 0; octave < 4; octave++) {
                    var sx = x * freq / size;
                    var sy = y * freq / size;
                    n += (Math.sin(sx * 41.2 + sy * 17.8) * 0.5 + 0.5) * amp;
                    n += (Math.sin(sx * 73.1 - sy * 29.4 + octave) * 0.5 + 0.5) * amp * 0.5;
                    amp *= 0.5;
                    freq *= 2.1;
                }
                n = Math.floor(118 + n * 22);
                i = (y * size + x) * 4;
                data[i] = n;
                data[i + 1] = n;
                data[i + 2] = n;
                data[i + 3] = 255;
            }
        }

        ctx.putImageData(imageData, 0, 0);
        var tex = new THREE.CanvasTexture(canvas);
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(3, 3);
        return tex;
    }

    function createBoxCardboardMaterial() {
        return new global.THREE.MeshStandardMaterial({
            color: BOX_CARDBOARD_COLOR,
            roughness: 0.9,
            metalness: 0,
            bumpMap: createCardboardBumpTexture(),
            bumpScale: 0.005,
        });
    }

    function createOpenCylinderGeometry(radius, height, segments) {
        return new global.THREE.CylinderGeometry(
            radius,
            radius,
            height,
            segments,
            1,
            true,
            0,
            FULL_CIRCLE
        );
    }

    function applyRadialUVsToRing(geometry, outerR) {
        var pos = geometry.attributes.position;
        var uv = geometry.attributes.uv;
        var scale = outerR * 2.15;
        var i;
        for (i = 0; i < pos.count; i++) {
            uv.setXY(i, pos.getX(i) / scale + 0.5, pos.getY(i) / scale + 0.5);
        }
        uv.needsUpdate = true;
    }

    function createRingCapGeometry(innerR, outerR, segments) {
        var geom = new global.THREE.RingGeometry(innerR, outerR, segments);
        applyRadialUVsToRing(geom, outerR);
        return geom;
    }

    function buildTapeRollGroup(THREE, materials, height) {
        var halfH = height / 2;
        var group = new THREE.Group();

        var outerShell = new THREE.Mesh(
            createOpenCylinderGeometry(TAPE_OUTER_R, height, 64),
            materials.outer
        );

        var capGeom = createRingCapGeometry(TAPE_INNER_R, TAPE_OUTER_R, 64);
        var capTop = new THREE.Mesh(capGeom, materials.cap);
        capTop.position.y = halfH;
        capTop.rotation.x = -Math.PI / 2;

        var capBottom = new THREE.Mesh(capGeom.clone(), materials.cap);
        capBottom.position.y = -halfH;
        capBottom.rotation.x = Math.PI / 2;

        var innerCore = new THREE.Mesh(
            createOpenCylinderGeometry(TAPE_INNER_R, height, 64),
            materials.cardboard
        );

        group.add(outerShell, capTop, capBottom, innerCore);

        return {
            group: group,
            outerShell: outerShell,
            capTop: capTop,
            capBottom: capBottom,
            innerCore: innerCore,
        };
    }

    function createTopEdgeTexture(hexColor, isTransparent) {
        var THREE = global.THREE;
        var size = 512;
        var cx = size / 2;
        var cy = size / 2;
        var maxR = size / 2 - 4;

        var colorCanvas = document.createElement('canvas');
        colorCanvas.width = size;
        colorCanvas.height = size;
        var ctx = colorCanvas.getContext('2d');

        ctx.fillStyle = hexColor;
        ctx.globalAlpha = isTransparent ? 0.55 : 1;
        ctx.fillRect(0, 0, size, size);
        ctx.globalAlpha = 1;

        var r;
        for (r = maxR; r > 8; r -= 1.1) {
            var t = 1 - r / maxR;
            ctx.strokeStyle = isTransparent
                ? 'rgba(71, 85, 105, ' + (0.15 + t * 0.25) + ')'
                : 'rgba(100, 100, 100, ' + (0.28 + t * 0.2) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.arc(cx, cy, r, 0, FULL_CIRCLE);
            ctx.stroke();
            ctx.strokeStyle = isTransparent
                ? 'rgba(255, 255, 255, ' + (0.08 + t * 0.12) + ')'
                : 'rgba(255, 255, 255, ' + (0.12 + t * 0.18) + ')';
            ctx.lineWidth = 0.55;
            ctx.beginPath();
            ctx.arc(cx, cy, r - 0.35, 0, FULL_CIRCLE);
            ctx.stroke();
        }

        var bumpCanvas = document.createElement('canvas');
        bumpCanvas.width = size;
        bumpCanvas.height = size;
        var bumpCtx = bumpCanvas.getContext('2d');
        bumpCtx.fillStyle = '#000000';
        bumpCtx.fillRect(0, 0, size, size);

        for (r = maxR; r > 8; r -= 1.1) {
            bumpCtx.strokeStyle = '#ffffff';
            bumpCtx.lineWidth = 1.6;
            bumpCtx.beginPath();
            bumpCtx.arc(cx, cy, r, 0, FULL_CIRCLE);
            bumpCtx.stroke();
        }

        var colorMap = new THREE.CanvasTexture(colorCanvas);
        colorMap.anisotropy = 8;
        var bumpMap = new THREE.CanvasTexture(bumpCanvas);
        bumpMap.anisotropy = 4;

        return { colorMap: colorMap, bumpMap: bumpMap };
    }

    function createCapEdgeMaterial(capTextures, isTransparent) {
        var THREE = global.THREE;
        var opts = {
            map: capTextures.colorMap,
            bumpMap: capTextures.bumpMap,
            bumpScale: 0.035,
            roughness: 0.1,
            metalness: TAPE_METALNESS,
            clearcoat: TAPE_CLEARCOAT,
            clearcoatRoughness: TAPE_CLEARCOAT_ROUGHNESS,
        };
        if (isTransparent) {
            opts.transparent = true;
            opts.opacity = TAPE_TRANSPARENT_OPACITY;
            opts.side = THREE.DoubleSide;
        }
        return new THREE.MeshPhysicalMaterial(opts);
    }

    function tapeMaterialColor(colorKey) {
        if (colorKey === 'hnědá') return 0x9c663b;
        return 0xffffff;
    }

    function createTapeMaterial(texture, colorKey) {
        var THREE = global.THREE;
        var isTransparent = colorKey === 'transparentní';
        var opts = {
            map: texture,
            color: tapeMaterialColor(colorKey),
            roughness: TAPE_ROUGHNESS,
            metalness: TAPE_METALNESS,
            clearcoat: TAPE_CLEARCOAT,
            clearcoatRoughness: TAPE_CLEARCOAT_ROUGHNESS,
        };
        if (isTransparent) {
            opts.transparent = true;
            opts.opacity = TAPE_TRANSPARENT_OPACITY;
            opts.side = THREE.DoubleSide;
        }
        return new THREE.MeshPhysicalMaterial(opts);
    }

    function applyTapeMaterialState(material, colorKey) {
        var THREE = global.THREE;
        var isTransparent = colorKey === 'transparentní';
        material.color.setHex(tapeMaterialColor(colorKey));
        material.roughness = TAPE_ROUGHNESS;
        material.metalness = TAPE_METALNESS;
        material.clearcoat = TAPE_CLEARCOAT;
        material.clearcoatRoughness = TAPE_CLEARCOAT_ROUGHNESS;
        material.transparent = isTransparent;
        material.opacity = isTransparent ? TAPE_TRANSPARENT_OPACITY : 1;
        material.side = isTransparent ? THREE.DoubleSide : THREE.FrontSide;
        material.needsUpdate = true;
    }

    function createCardboardMaterial() {
        return new global.THREE.MeshStandardMaterial({
            color: CARDBOARD_CORE_COLOR,
            roughness: 0.9,
            metalness: 0,
            side: global.THREE.BackSide,
        });
    }

    function TapeConfigurator3D(container) {
        if (!container || !global.THREE) return null;

        var self = this;

        this.container = container;
        this.state = {
            colorKey: 'bílá',
            widthMm: 50,
            text: '',
            textColor: '#1e293b',
            textSize: 40,
            textOffsetY: 0,
            fontFamily: 'Plus Jakarta Sans',
            motifSpacing: 80,
            logoImage: null,
            boxMode: false,
        };

        this.rotation = { x: 0.25, y: 0.6 };
        this.isDragging = false;
        this.pointer = { x: 0, y: 0 };
        this.animationId = null;
        this.lookAtTarget = { x: 0, y: 0, z: 0 };

        this._initScene();
        this._buildModels();
        this._bindPointer();
        this._bindResize();
        this._animate();
        this.syncFromForm();
    }

    TapeConfigurator3D.prototype._initScene = function () {
        var THREE = global.THREE;
        var w = this.container.clientWidth || 320;
        var h = this.container.clientHeight || 320;

        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xffffff);

        this.camera = new THREE.PerspectiveCamera(42, w / h, 0.1, 100);
        this.camera.position.set(0, 0.6, 8);
        this.camera.lookAt(0, 0, 0);

        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
        this.renderer.setPixelRatio(Math.min(global.devicePixelRatio || 1, 2));
        this.renderer.setSize(w, h);
        this.renderer.setClearColor(0xffffff, 1);
        this.renderer.shadowMap.enabled = false;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.0;
        this.container.innerHTML = '';
        this.container.appendChild(this.renderer.domElement);

        var ambient = new THREE.AmbientLight(0xffffff, 0.52);

        var key = new THREE.DirectionalLight(0xffffff, 1.5);
        key.position.set(2, 8, 6);

        var fill = new THREE.DirectionalLight(0xfff8f0, 0.35);
        fill.position.set(-4, 3, -3);

        this.scene.add(ambient, key, fill);
    };

    TapeConfigurator3D.prototype._createTapeTexture = function () {
        var THREE = global.THREE;
        var canvas = document.createElement('canvas');
        canvas.width = CANVAS_W;
        canvas.height = CANVAS_H;
        this.textureCanvas = canvas;
        this.textureCtx = canvas.getContext('2d');
        this.tapeTexture = new THREE.CanvasTexture(canvas);
        this.tapeTexture.wrapS = THREE.RepeatWrapping;
        this.tapeTexture.wrapT = THREE.ClampToEdgeWrapping;
        this.tapeTexture.repeat.set(TAPE_ROLL_TEXTURE_REPEAT, 1);
        this.tapeTexture.anisotropy = 8;

        this.boxTapeTexture = this.tapeTexture.clone();
        configureBoxTapeTexture(this.boxTapeTexture);
        var boxRepeat = getBoxTapeTextureRepeat(BASE_WIDTH_MM);
        this.boxTapeTexture.repeat.set(boxRepeat.u, boxRepeat.v);

        this._drawTapeTexture();
        return this.tapeTexture;
    };

    TapeConfigurator3D.prototype._hexFromColorKey = function (key) {
        var hex = COLOR_MAP[key] || COLOR_MAP['bílá'];
        return '#' + hex.toString(16).padStart(6, '0');
    };

    TapeConfigurator3D.prototype._contentY = function (canvas) {
        return canvas.height * 0.5 + (this.state.textOffsetY / 50) * (canvas.height * 0.22);
    };

    TapeConfigurator3D.prototype._drawLogoMotif = function (ctx, canvas, centerY) {
        var img = this.state.logoImage;
        if (!img || !img.complete) return;

        var maxH = canvas.height * 0.72;
        var scale = (this.state.textSize / 40) * maxH * 0.85;
        var ratio = img.width / img.height;
        var drawH = Math.min(maxH, scale);
        var drawW = drawH * ratio;
        var gap = this.state.motifSpacing;
        var step = drawW + gap;

        for (var x = -drawW; x < canvas.width + drawW; x += step) {
            ctx.drawImage(img, x, centerY - drawH * 0.5, drawW, drawH);
        }
    };

    TapeConfigurator3D.prototype._drawTextMotif = function (ctx, canvas, centerY) {
        var label = (this.state.text || 'VÁŠ TEXT').toUpperCase();
        var fontFamily = this.state.fontFamily || 'Plus Jakarta Sans';
        var textSize = this.state.textSize || 40;

        ctx.fillStyle = this.state.textColor || '#1e293b';
        ctx.font = 'bold ' + textSize + 'px "' + fontFamily + '", Arial, system-ui, sans-serif';
        ctx.textBaseline = 'middle';
        ctx.textAlign = 'left';

        var metrics = ctx.measureText(label);
        var gap = this.state.motifSpacing;
        var step = metrics.width + gap;

        for (var x = -step; x < canvas.width + step; x += step) {
            ctx.fillText(label, x, centerY);
        }
    };

    TapeConfigurator3D.prototype._drawTapeTexture = function () {
        var ctx = this.textureCtx;
        var canvas = this.textureCanvas;
        if (!ctx || !canvas) return;

        var isTransparent = this.state.colorKey === 'transparentní';
        var centerY = this._contentY(canvas);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ffffff';
        ctx.globalAlpha = isTransparent ? 0.2 : 1;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 1;

        if (isTransparent) {
            ctx.strokeStyle = 'rgba(148, 163, 184, 0.35)';
            for (var i = 0; i < canvas.width; i += 24) {
                ctx.beginPath();
                ctx.moveTo(i, 0);
                ctx.lineTo(i + canvas.height, canvas.height);
                ctx.stroke();
            }
        }

        if (this.state.logoImage) {
            this._drawLogoMotif(ctx, canvas, centerY);
        } else {
            this._drawTextMotif(ctx, canvas, centerY);
        }

        this.tapeTexture.needsUpdate = true;
        if (this.boxTapeTexture) {
            this.boxTapeTexture.needsUpdate = true;
        }
        if (this.boxTapeMat) {
            this.boxTapeMat.map = this.boxTapeTexture;
            this.boxTapeMat.needsUpdate = true;
        }
        if (this.tapeMaterial) {
            this.tapeMaterial.map = this.tapeTexture;
            this.tapeMaterial.needsUpdate = true;
        }

        this._drawBoxPatchTexture();
    };

    TapeConfigurator3D.prototype._createBoxPatchTexture = function () {
        var THREE = global.THREE;
        var canvas = document.createElement('canvas');
        canvas.width = PATCH_CANVAS_SIZE;
        canvas.height = PATCH_CANVAS_SIZE;
        this.patchCanvas = canvas;
        this.patchCtx = canvas.getContext('2d');
        this.boxPatchTexture = new THREE.CanvasTexture(canvas);
        this.boxPatchTexture.minFilter = THREE.LinearFilter;
        this.boxPatchTexture.magFilter = THREE.LinearFilter;
        this.boxPatchTexture.generateMipmaps = false;
        this.boxPatchTexture.anisotropy = 8;
        this._drawBoxPatchTexture();
        return this.boxPatchTexture;
    };

    TapeConfigurator3D.prototype._drawBoxPatchTexture = function () {
        var ctx = this.patchCtx;
        var canvas = this.patchCanvas;
        if (!ctx || !canvas) return;

        var isTransparent = this.state.colorKey === 'transparentní';
        var centerY = canvas.height * 0.5 + (this.state.textOffsetY / 50) * (canvas.height * 0.12);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ffffff';
        ctx.globalAlpha = isTransparent ? 0.2 : 1;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 1;

        if (isTransparent) {
            ctx.strokeStyle = 'rgba(148, 163, 184, 0.35)';
            for (var i = 0; i < canvas.width; i += 24) {
                ctx.beginPath();
                ctx.moveTo(i, 0);
                ctx.lineTo(i + canvas.height, canvas.height);
                ctx.stroke();
            }
        }

        if (this.state.logoImage && this.state.logoImage.complete) {
            var img = this.state.logoImage;
            var maxH = canvas.height * 0.72;
            var scale = (this.state.textSize / 40) * maxH * 0.85;
            var ratio = img.width / img.height;
            var drawH = Math.min(maxH, scale);
            var drawW = drawH * ratio;
            ctx.drawImage(img, (canvas.width - drawW) * 0.5, centerY - drawH * 0.5, drawW, drawH);
        } else {
            var label = (this.state.text || 'VÁŠ TEXT').toUpperCase();
            var fontFamily = this.state.fontFamily || 'Plus Jakarta Sans';
            var textSize = Math.round((this.state.textSize || 40) * (canvas.height / CANVAS_H) * 1.35);
            ctx.fillStyle = this.state.textColor || '#1e293b';
            ctx.font = 'bold ' + textSize + 'px "' + fontFamily + '", Arial, system-ui, sans-serif';
            ctx.textBaseline = 'middle';
            ctx.textAlign = 'center';
            ctx.fillText(label, canvas.width * 0.5, centerY);
        }

        if (this.boxPatchTexture) {
            this.boxPatchTexture.needsUpdate = true;
        }
        if (this.boxTapePatchMat) {
            this.boxTapePatchMat.map = this.boxPatchTexture;
            this.boxTapePatchMat.needsUpdate = true;
        }
    };

    TapeConfigurator3D.prototype._buildModels = function () {
        var THREE = global.THREE;
        this._createTapeTexture();
        var colorKey = this.state.colorKey;

        this.tapeMaterial = createTapeMaterial(this.tapeTexture, colorKey);
        this.tapeCardboardMaterial = createCardboardMaterial();
        this.tapeCapMaterial = createCapEdgeMaterial(
            createTopEdgeTexture(this._hexFromColorKey(colorKey), colorKey === 'transparentní'),
            colorKey === 'transparentní'
        );

        var roll = buildTapeRollGroup(THREE, {
            outer: this.tapeMaterial,
            cap: this.tapeCapMaterial,
            cardboard: this.tapeCardboardMaterial,
        }, TAPE_HEIGHT);

        this.tapeGroup = roll.group;
        this.tapeOuterShell = roll.outerShell;
        this.tapeCapTop = roll.capTop;
        this.tapeCapBottom = roll.capBottom;
        this.tapeInnerCore = roll.innerCore;
        this.scene.add(this.tapeGroup);

        this.boxGroup = new THREE.Group();
        this.boxGroup.visible = false;

        var boxMat = createBoxCardboardMaterial();
        this.cardboardBox = new THREE.Mesh(
            new THREE.BoxGeometry(BOX_WIDTH, BOX_HEIGHT, BOX_DEPTH),
            boxMat
        );

        this.boxTapeMat = createBoxTapeMaterial(this.boxTapeTexture, colorKey);
        var boxTape = buildBoxTapeGroup(THREE, this.boxTapeMat, BOX_TAPE_DEPTH);
        this.boxTapeGroup = boxTape.group;
        this.boxTapeTop = boxTape.topTape;
        this.boxTapeFront = boxTape.frontTape;
        this.boxTapeBack = boxTape.backTape;

        var boxCrossTape = buildBoxCrossTapeGroup(THREE, this.boxTapeMat, BOX_TAPE_DEPTH);
        this.boxCrossTapeGroup = boxCrossTape.group;
        this.boxCrossTapeTop = boxCrossTape.topTape;
        this.boxCrossTapeLeft = boxCrossTape.leftTape;
        this.boxCrossTapeRight = boxCrossTape.rightTape;

        this._createBoxPatchTexture();
        this.boxTapePatchMat = createBoxTapePatchMaterial(this.boxPatchTexture, colorKey);
        this.boxIntersectionPatch = buildBoxIntersectionPatch(THREE, this.boxTapePatchMat, BOX_TAPE_DEPTH);

        this.boxGroup.add(
            this.cardboardBox,
            this.boxTapeGroup,
            this.boxCrossTapeGroup,
            this.boxIntersectionPatch
        );
        this.scene.add(this.boxGroup);

        this._applyWidth(this.state.widthMm);
        this.setBoxMode(this.state.boxMode);
    };

    TapeConfigurator3D.prototype._activeGroup = function () {
        return this.state.boxMode ? this.boxGroup : this.tapeGroup;
    };

    TapeConfigurator3D.prototype._applyWidth = function (widthMm) {
        var w = parseInt(widthMm, 10) || BASE_WIDTH_MM;
        var scale = w / BASE_WIDTH_MM;

        if (this.tapeGroup) {
            this.tapeGroup.scale.y = scale;
        }

        var tapeWidth = BOX_TAPE_DEPTH * scale;

        if (this.boxTapeTop) {
            resizeBoxTapePlanes({
                topTape: this.boxTapeTop,
                frontTape: this.boxTapeFront,
                backTape: this.boxTapeBack,
            }, tapeWidth);
        }

        if (this.boxCrossTapeTop) {
            resizeBoxCrossTapePlanes({
                topTape: this.boxCrossTapeTop,
                leftTape: this.boxCrossTapeLeft,
                rightTape: this.boxCrossTapeRight,
            }, tapeWidth);
        }

        if (this.boxIntersectionPatch) {
            resizeBoxIntersectionPatch(this.boxIntersectionPatch, tapeWidth);
        }

        if (this.tapeTexture) {
            this.tapeTexture.repeat.set(TAPE_ROLL_TEXTURE_REPEAT, 1 / scale);
        }
        if (this.boxTapeTexture) {
            var boxRepeat = getBoxTapeTextureRepeat(w);
            this.boxTapeTexture.repeat.set(boxRepeat.u, boxRepeat.v);
            this.boxTapeTexture.needsUpdate = true;
        }
    };

    TapeConfigurator3D.prototype._applyColor = function (colorKey) {
        applyTapeMaterialState(this.tapeMaterial, colorKey);
        applyBoxTapeMaterialState(this.boxTapeMat, colorKey);
        if (this.boxTapePatchMat) {
            applyBoxTapePatchMaterialState(this.boxTapePatchMat, colorKey);
        }
        if (this.boxTapeTexture) {
            this.boxTapeMat.map = this.boxTapeTexture;
        }
        if (this.boxPatchTexture && this.boxTapePatchMat) {
            this.boxTapePatchMat.map = this.boxPatchTexture;
        }

        this._drawTapeTexture();
        this._refreshCapEdgeMaterials(colorKey);
    };

    TapeConfigurator3D.prototype._refreshCapEdgeMaterials = function (colorKey) {
        var isTransparent = colorKey === 'transparentní';
        var hex = this._hexFromColorKey(colorKey);

        if (this.tapeCapMaterial) {
            if (this.tapeCapMaterial.map) this.tapeCapMaterial.map.dispose();
            if (this.tapeCapMaterial.bumpMap) this.tapeCapMaterial.bumpMap.dispose();
            this.tapeCapMaterial.dispose();
        }

        this.tapeCapMaterial = createCapEdgeMaterial(
            createTopEdgeTexture(hex, isTransparent),
            isTransparent
        );

        if (this.tapeCapTop) this.tapeCapTop.material = this.tapeCapMaterial;
        if (this.tapeCapBottom) this.tapeCapBottom.material = this.tapeCapMaterial;
    };

    TapeConfigurator3D.prototype.setStudioBackground = function (hexColor) {
        if (!this.scene) return;
        this.scene.background = new global.THREE.Color(hexColor);
        this.renderer.setClearColor(hexColor, 1);
    };

    TapeConfigurator3D.prototype.setColor = function (colorKey) {
        this.state.colorKey = colorKey || 'bílá';
        this._applyColor(this.state.colorKey);
    };

    TapeConfigurator3D.prototype.setWidth = function (widthMm) {
        var w = parseInt(widthMm, 10) || BASE_WIDTH_MM;
        this.state.widthMm = w;
        this._applyWidth(w);
    };

    TapeConfigurator3D.prototype.setText = function (text) {
        this.state.text = text || '';
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.setTextColor = function (hex) {
        this.state.textColor = hex || '#1e293b';
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.setTextSize = function (size) {
        this.state.textSize = parseInt(size, 10) || 40;
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.setTextOffsetY = function (offset) {
        this.state.textOffsetY = parseInt(offset, 10) || 0;
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.setFontFamily = function (font) {
        this.state.fontFamily = font || 'Plus Jakarta Sans';
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.setMotifSpacing = function (spacing) {
        this.state.motifSpacing = parseInt(spacing, 10) || 80;
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.setLogo = function (image) {
        this.state.logoImage = image || null;
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.clearLogo = function () {
        this.state.logoImage = null;
        this._drawTapeTexture();
    };

    TapeConfigurator3D.prototype.setBoxMode = function (enabled) {
        this.state.boxMode = !!enabled;
        if (this.tapeGroup) this.tapeGroup.visible = !this.state.boxMode;
        if (this.boxGroup) this.boxGroup.visible = this.state.boxMode;
        this.lookAtTarget = { x: 0, y: 0, z: 0 };
        this.rotation = { x: 0.25, y: 0.6 };
        if (this.camera) {
            this.camera.lookAt(0, 0, 0);
        }
    };

    TapeConfigurator3D.prototype.syncFromForm = function () {
        var form = document.getElementById('gform_1');
        var modal = document.getElementById('tape-3d-modal');
        if (!form) return;

        var color = modal
            ? modal.querySelector('input[name="modal_input_9"]:checked')
            : form.querySelector('input[name="input_9"]:checked');
        var width = modal
            ? modal.querySelector('input[name="modal_input_12"]:checked')
            : form.querySelector('input[name="input_12"]:checked');
        var textInput = document.getElementById('tape-print-text');
        var textColorHidden = document.getElementById('tape-text-color-value');
        var textColorRadio = modal
            ? modal.querySelector('input[name="tape_text_color"]:checked')
            : null;
        var textSizeInput = document.getElementById('tape-text-size');
        var textOffsetInput = document.getElementById('tape-text-offset');
        var fontRadio = modal
            ? modal.querySelector('input[name="tape_font_family"]:checked')
            : null;
        var fontForm = document.getElementById('tape-font-form');
        var spacingInput = document.getElementById('tape-motif-spacing');

        if (color) this.setColor(color.value);
        if (width) this.setWidth(width.value);
        if (textInput) this.setText(textInput.value);
        if (textColorHidden && textColorHidden.value) {
            this.setTextColor(textColorHidden.value);
        } else if (textColorRadio) {
            this.setTextColor(textColorRadio.value);
        }
        if (textSizeInput) this.setTextSize(textSizeInput.value);
        if (textOffsetInput) this.setTextOffsetY(textOffsetInput.value);
        if (fontRadio) {
            this.setFontFamily(fontRadio.value);
        } else if (fontForm) {
            this.setFontFamily(fontForm.value);
        }
        if (spacingInput) this.setMotifSpacing(spacingInput.value);
    };

    TapeConfigurator3D.prototype.resize = function () {
        if (!this.container || !this.renderer) return;
        var w = this.container.clientWidth;
        var h = this.container.clientHeight;
        if (w < 1 || h < 1) return;
        this.camera.aspect = w / h;
        this.camera.updateProjectionMatrix();
        this.camera.lookAt(this.lookAtTarget.x, this.lookAtTarget.y, this.lookAtTarget.z);
        this.renderer.setSize(w, h);
    };

    TapeConfigurator3D.prototype._bindPointer = function () {
        var self = this;
        var el = this.renderer.domElement;

        el.style.touchAction = 'none';

        function onDown(e) {
            self.isDragging = true;
            self.pointer.x = e.clientX;
            self.pointer.y = e.clientY;
            el.setPointerCapture(e.pointerId);
        }

        function onMove(e) {
            if (!self.isDragging) return;
            var dx = e.clientX - self.pointer.x;
            var dy = e.clientY - self.pointer.y;
            self.rotation.y += dx * 0.012;
            self.rotation.x += dy * 0.012;
            self.rotation.x = Math.max(-0.9, Math.min(0.9, self.rotation.x));
            self.pointer.x = e.clientX;
            self.pointer.y = e.clientY;
        }

        function onUp(e) {
            self.isDragging = false;
            try { el.releasePointerCapture(e.pointerId); } catch (err) { /* noop */ }
        }

        el.addEventListener('pointerdown', onDown);
        el.addEventListener('pointermove', onMove);
        el.addEventListener('pointerup', onUp);
        el.addEventListener('pointerleave', onUp);
    };

    TapeConfigurator3D.prototype._bindResize = function () {
        var self = this;
        if (typeof ResizeObserver !== 'undefined') {
            this._resizeObserver = new ResizeObserver(function () { self.resize(); });
            this._resizeObserver.observe(this.container);
        } else {
            global.addEventListener('resize', function () { self.resize(); });
        }
    };

    TapeConfigurator3D.prototype._animate = function () {
        var self = this;
        function frame() {
            self.animationId = global.requestAnimationFrame(frame);
            var group = self._activeGroup();
            if (group) {
                if (!self.isDragging) {
                    self.rotation.y += 0.003;
                }
                group.rotation.x = self.rotation.x;
                group.rotation.y = self.rotation.y;
            }
            self.camera.lookAt(self.lookAtTarget.x, self.lookAtTarget.y, self.lookAtTarget.z);
            self.renderer.render(self.scene, self.camera);
        }
        frame();
    };

    TapeConfigurator3D.prototype.dispose = function () {
        if (this.animationId) global.cancelAnimationFrame(this.animationId);
        if (this._resizeObserver) this._resizeObserver.disconnect();
        if (this.renderer) this.renderer.dispose();
    };

    function syncHiddenFields() {
        var textInput = document.getElementById('tape-print-text');
        var textForm = document.getElementById('tape-print-text-form');
        if (textInput && textForm) textForm.value = textInput.value;

        var colorHidden = document.getElementById('tape-text-color-value');
        var modal = document.getElementById('tape-3d-modal');
        var colorRadio = modal ? modal.querySelector('input[name="tape_text_color"]:checked') : null;
        var colorCustom = document.getElementById('tape-text-color-custom');
        if (colorHidden) {
            if (colorRadio) colorHidden.value = colorRadio.value;
            else if (colorCustom) colorHidden.value = colorCustom.value;
        }

        var sizeInput = document.getElementById('tape-text-size');
        var sizeForm = document.getElementById('tape-text-size-form');
        if (sizeInput && sizeForm) sizeForm.value = sizeInput.value;

        var offsetInput = document.getElementById('tape-text-offset');
        var offsetForm = document.getElementById('tape-text-offset-form');
        if (offsetInput && offsetForm) offsetForm.value = offsetInput.value;

        var fontForm = document.getElementById('tape-font-form');
        var fontRadio = modal ? modal.querySelector('input[name="tape_font_family"]:checked') : null;
        if (fontRadio && fontForm) fontForm.value = fontRadio.value;

        var spacingInput = document.getElementById('tape-motif-spacing');
        var spacingForm = document.getElementById('tape-motif-spacing-form');
        if (spacingInput && spacingForm) spacingForm.value = spacingInput.value;
    }

    function syncFormRadiosFromModal() {
        var form = document.getElementById('gform_1');
        var modal = document.getElementById('tape-3d-modal');
        if (!form || !modal) return;

        var modalMaterial = modal.querySelector('input[name="modal_input_8"]:checked');
        var modalColor = modal.querySelector('input[name="modal_input_9"]:checked');
        var modalWidth = modal.querySelector('input[name="modal_input_12"]:checked');
        var modalLength = modal.querySelector('input[name="modal_input_11"]:checked');
        if (modalMaterial) {
            var f = form.querySelector('input[name="input_8"][value="' + modalMaterial.value + '"]');
            if (f) f.checked = true;
        }
        if (modalColor) {
            var fc = form.querySelector('input[name="input_9"][value="' + modalColor.value + '"]');
            if (fc) fc.checked = true;
        }
        if (modalWidth) {
            var fw = form.querySelector('input[name="input_12"][value="' + modalWidth.value + '"]');
            if (fw) fw.checked = true;
        }
        if (modalLength) {
            var fl = form.querySelector('input[name="input_11"][value="' + modalLength.value + '"]');
            if (fl) fl.checked = true;
        }
    }

    function initAccordion() {
        var accordion = document.getElementById('tape-config-accordion');
        if (!accordion) return;

        var items = accordion.querySelectorAll('[data-accordion-item]');

        function closeAll(except) {
            items.forEach(function (item) {
                if (item === except) return;
                item.classList.remove('is-open');
                var trigger = item.querySelector('[data-accordion-trigger]');
                if (trigger) trigger.setAttribute('aria-expanded', 'false');
            });
        }

        items.forEach(function (item) {
            var trigger = item.querySelector('[data-accordion-trigger]');
            var panel = item.querySelector('.tape-accordion-panel');
            if (!trigger) return;

            if (panel) {
                panel.addEventListener('click', function (e) {
                    e.stopPropagation();
                });
            }

            trigger.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                var isOpen = item.classList.contains('is-open');
                if (isOpen) {
                    item.classList.remove('is-open');
                    trigger.setAttribute('aria-expanded', 'false');
                    return;
                }
                closeAll(item);
                item.classList.add('is-open');
                trigger.setAttribute('aria-expanded', 'true');
            });
        });
    }

    function bindStudioBackground(configurator) {
        var picker = document.getElementById('tape-studio-bg');
        if (!picker || !configurator) return;

        var dots = picker.querySelectorAll('[data-studio-bg]');
        dots.forEach(function (dot) {
            dot.addEventListener('click', function (e) {
                e.stopPropagation();
                var hex = dot.getAttribute('data-studio-bg');
                if (!hex) return;
                configurator.setStudioBackground(parseInt(hex, 16));
                dots.forEach(function (d) { d.classList.remove('is-active'); });
                dot.classList.add('is-active');
            });
        });
    }

    function updateLogoUI(filename) {
        var filenameEl = document.getElementById('tape-logo-filename');
        var removeBtn = document.getElementById('tape-logo-remove');
        var uploadBtn = document.getElementById('tape-logo-upload-btn');

        if (filename) {
            if (filenameEl) {
                filenameEl.textContent = 'Nahráno: ' + filename;
                filenameEl.classList.remove('hidden');
            }
            if (removeBtn) removeBtn.classList.remove('hidden');
            if (uploadBtn) uploadBtn.classList.add('border-orange-300', 'bg-orange-50', 'text-orange-700');
        } else {
            if (filenameEl) {
                filenameEl.textContent = '';
                filenameEl.classList.add('hidden');
            }
            if (removeBtn) removeBtn.classList.add('hidden');
            if (uploadBtn) uploadBtn.classList.remove('border-orange-300', 'bg-orange-50', 'text-orange-700');
        }
    }

    function bindForm(configurator) {
        var form = document.getElementById('gform_1');
        var modal = document.getElementById('tape-3d-modal');
        if (!form || !configurator) return;

        if (modal) {
            modal.querySelectorAll('input[name="modal_input_9"]').forEach(function (el) {
                el.addEventListener('change', function () {
                    configurator.setColor(el.value);
                    syncFormRadiosFromModal();
                    syncHiddenFields();
                });
            });

            modal.querySelectorAll('input[name="modal_input_8"]').forEach(function (el) {
                el.addEventListener('change', function () {
                    syncFormRadiosFromModal();
                    syncHiddenFields();
                });
            });

            modal.querySelectorAll('input[name="modal_input_12"]').forEach(function (el) {
                el.addEventListener('change', function () {
                    configurator.setWidth(el.value);
                    syncFormRadiosFromModal();
                    syncHiddenFields();
                });
            });

            modal.querySelectorAll('input[name="modal_input_11"]').forEach(function (el) {
                el.addEventListener('change', function () {
                    syncFormRadiosFromModal();
                    syncHiddenFields();
                });
            });
        }

        form.querySelectorAll('input[name="input_12"]').forEach(function (el) {
            el.addEventListener('change', function () {
                var modal = document.getElementById('tape-3d-modal');
                var modalRadio = modal && modal.querySelector('input[name="modal_input_12"][value="' + el.value + '"]');
                if (modalRadio) modalRadio.checked = true;
                configurator.setWidth(el.value);
            });
        });

        var textInput = document.getElementById('tape-print-text');
        if (textInput) {
            textInput.addEventListener('input', function () {
                configurator.setText(textInput.value);
                syncHiddenFields();
            });
        }

        var colorHidden = document.getElementById('tape-text-color-value');
        var colorCustom = document.getElementById('tape-text-color-custom');

        function applyTextColor(hex) {
            if (colorHidden) colorHidden.value = hex;
            configurator.setTextColor(hex);
            syncHiddenFields();
        }

        var colorScope = modal || form;
        colorScope.querySelectorAll('input[name="tape_text_color"]').forEach(function (el) {
            el.addEventListener('change', function () {
                if (colorCustom) colorCustom.value = el.value;
                applyTextColor(el.value);
            });
        });

        if (colorCustom) {
            colorCustom.addEventListener('input', function () {
                colorScope.querySelectorAll('input[name="tape_text_color"]').forEach(function (r) { r.checked = false; });
                applyTextColor(colorCustom.value);
            });
        }

        var fontScope = modal || form;
        fontScope.querySelectorAll('input[name="tape_font_family"]').forEach(function (el) {
            el.addEventListener('change', function () {
                configurator.setFontFamily(el.value);
                syncHiddenFields();
            });
        });

        var textSizeInput = document.getElementById('tape-text-size');
        var textSizeLabel = document.getElementById('tape-text-size-value');
        if (textSizeInput) {
            textSizeInput.addEventListener('input', function () {
                if (textSizeLabel) textSizeLabel.textContent = textSizeInput.value;
                configurator.setTextSize(textSizeInput.value);
                syncHiddenFields();
            });
        }

        var textOffsetInput = document.getElementById('tape-text-offset');
        var textOffsetLabel = document.getElementById('tape-text-offset-value');
        if (textOffsetInput) {
            textOffsetInput.addEventListener('input', function () {
                if (textOffsetLabel) textOffsetLabel.textContent = textOffsetInput.value;
                configurator.setTextOffsetY(textOffsetInput.value);
                syncHiddenFields();
            });
        }

        var spacingInput = document.getElementById('tape-motif-spacing');
        var spacingLabel = document.getElementById('tape-motif-spacing-value');
        if (spacingInput) {
            spacingInput.addEventListener('input', function () {
                if (spacingLabel) spacingLabel.textContent = spacingInput.value;
                configurator.setMotifSpacing(spacingInput.value);
                syncHiddenFields();
            });
        }

        var logoUpload = document.getElementById('tape-logo-upload');
        var logoUploadBtn = document.getElementById('tape-logo-upload-btn');
        var logoRemove = document.getElementById('tape-logo-remove');

        if (logoUploadBtn && logoUpload) {
            logoUploadBtn.addEventListener('click', function () { logoUpload.click(); });
        }

        if (logoUpload) {
            logoUpload.addEventListener('change', function () {
                var file = logoUpload.files && logoUpload.files[0];
                if (!file) return;

                var reader = new FileReader();
                reader.onload = function (ev) {
                    var img = new Image();
                    img.onload = function () {
                        configurator.setLogo(img);
                        updateLogoUI(file.name);
                    };
                    img.src = ev.target.result;
                };
                reader.readAsDataURL(file);
            });
        }

        if (logoRemove) {
            logoRemove.addEventListener('click', function () {
                configurator.clearLogo();
                if (logoUpload) logoUpload.value = '';
                updateLogoUI(null);
            });
        }

        var toggle = document.getElementById('tape-3d-box-toggle');
        if (toggle) {
            toggle.addEventListener('click', function () {
                var on = toggle.getAttribute('aria-pressed') !== 'true';
                toggle.setAttribute('aria-pressed', on ? 'true' : 'false');
                toggle.textContent = on ? 'Zobrazit samotnou pásku' : 'Zobrazit na krabici';
                toggle.classList.toggle('bg-orange-600', on);
                toggle.classList.toggle('text-white', on);
                toggle.classList.toggle('border-orange-600', on);
                toggle.classList.toggle('bg-white', !on);
                toggle.classList.toggle('text-slate-700', !on);
                toggle.classList.toggle('border-slate-200', !on);
                configurator.setBoxMode(on);
            });
        }
    }

    function init() {
        initAccordion();
        var container = document.getElementById('tape-3d-preview');
        if (!container || !global.THREE) return null;
        var instance = new TapeConfigurator3D(container);
        bindForm(instance);
        bindStudioBackground(instance);
        global.TapeConfigurator3D = instance;
        return instance;
    }

    global.initTapeConfigurator3D = init;
})(window);
