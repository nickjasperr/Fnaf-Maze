
   var strVertexShaderSource =
    'attribute vec3 vertexPos;\n' +
    'attribute vec4 vertexColor;\n' +
    'attribute vec2 vertexTexCoord;\n' +
    'uniform mat4 modelViewMatrix;\n' +
    'uniform mat4 projectionMatrix;\n' +
    'varying vec4 vColor;\n' +
    'varying vec2 vTexCoord;\n' +
    'void main(void) {\n' +
    '    gl_Position = projectionMatrix * modelViewMatrix * vec4(vertexPos, 1.0);\n' +
    '    vColor = vertexColor;\n' +
    '    vTexCoord = vertexTexCoord;\n' +
    '}\n';

    var strFragmentShaderSource =
    'precision mediump float;\n' +
    'varying vec4 vColor;\n' +
    'varying vec2 vTexCoord;\n' +
    'uniform sampler2D uTexture;\n' +
    'uniform int useTexture;\n' +
    'void main(void) {\n' +
    '    if (useTexture == 1) {\n' +
    '        gl_FragColor = texture2D(uTexture, vTexCoord);\n' +
    '    } else {\n' +
    '        gl_FragColor = vColor;\n' +
    '    }\n' +
    '}\n';

     function creerShader(objgl, strSource, strType) {
        var objShader = null;
		
        if (strType == 'fragment') {
            objShader = objgl.createShader(objgl.FRAGMENT_SHADER);
        } else if (strType == 'vertex') {
            objShader = objgl.createShader(objgl.VERTEX_SHADER);
        } 
		
		if (!objShader) {
			alert('Impossible de créer le ' + strType + 'shader');
		}
		else {
			objgl.shaderSource(objShader, strSource);
			objgl.compileShader(objShader);
			if (!objgl.getShaderParameter(objShader, objgl.COMPILE_STATUS)) {
				alert('Impossible de compiler le ' + strType + ' shader');
			}
        }

        return objShader;
    }

	function initShaders(objgl) {
		var objProgShaders = null;

		// Créer les shaders à partir du code source
        var objFragmentShader = creerShader(objgl, strFragmentShaderSource, 'fragment');
        var objVertexShader = creerShader(objgl, strVertexShaderSource, 'vertex');
		
		if (objFragmentShader && objVertexShader) { 
		    // Créer le programme qui va exécuter les shaders
			objProgShaders = objgl.createProgram();
			objgl.attachShader(objProgShaders, objVertexShader);
			objgl.attachShader(objProgShaders, objFragmentShader);
			objgl.linkProgram(objProgShaders);
			objgl.enable(objgl.CULL_FACE);
			objgl.cullFace(objgl.BACK);
			objgl.frontFace(objgl.CCW);
		
			if (!objgl.getProgramParameter(objProgShaders, objgl.LINK_STATUS)) {
				alert('Impossible de lier les shaders');
			}
			else {	
				objProgShaders.posVertex = objgl.getAttribLocation(objProgShaders, 'vertexPos');
				objgl.enableVertexAttribArray(objProgShaders.posVertex);

				objProgShaders.couleurVertex = objgl.getAttribLocation(objProgShaders, 'vertexColor');
				objgl.enableVertexAttribArray(objProgShaders.couleurVertex);

				objProgShaders.texCoord = objgl.getAttribLocation(objProgShaders, 'vertexTexCoord');
				objgl.enableVertexAttribArray(objProgShaders.texCoord);

				objProgShaders.matProjection = objgl.getUniformLocation(objProgShaders, 'projectionMatrix');
				objProgShaders.matModeleVue = objgl.getUniformLocation(objProgShaders, 'modelViewMatrix');
				objProgShaders.uTexture = objgl.getUniformLocation(objProgShaders, 'uTexture');
				objProgShaders.useTexture = objgl.getUniformLocation(objProgShaders, 'useTexture');

				objgl.useProgram(objProgShaders);
			}
		}
		
		return objProgShaders;
    }
