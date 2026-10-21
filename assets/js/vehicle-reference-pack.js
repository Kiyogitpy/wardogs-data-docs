/* Local-only cooked reference packs. No file contents are uploaded or fetched. */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./vehicle-cooked-queries.js'));
  else root.VehicleReferencePack = factory(root.VehicleCookedQueries);
}(typeof globalThis !== 'undefined' ? globalThis : this, function (queries) {
  'use strict';
  const BUILD = 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37';
  const encoder = new TextEncoder();
  function fail(message) { throw new Error(message); }
  async function digest(bytes) {
    if (!globalThis.crypto || !globalThis.crypto.subtle) fail('Open the viewer over HTTPS or localhost to verify a reference pack.');
    return Array.from(new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256', bytes)), b => b.toString(16).padStart(2, '0')).join('');
  }
  async function verified(bytes, expected, label) {
    if (!/^[0-9a-f]{64}$/.test(expected) || await digest(bytes) !== expected) fail(label + ' failed its integrity check. Export the pack again.');
  }
  function decode(text) {
    const binary = atob(text), bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return bytes;
  }
  function selfContainedMesh(bytes) {
    if (bytes.length < 20) fail('Invalid reference collision mesh.');
    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    if (view.getUint32(0, true) !== 0x46546c67 || view.getUint32(4, true) !== 2 || view.getUint32(8, true) !== bytes.length ||
        view.getUint32(16, true) !== 0x4e4f534a || view.getUint32(12, true) > bytes.length - 20) fail('Invalid reference collision mesh.');
    let gltf;
    try { gltf = JSON.parse(new TextDecoder().decode(bytes.subarray(20, 20 + view.getUint32(12, true)))); }
    catch (_) { fail('Invalid reference collision mesh JSON.'); }
    function visit(value) {
      if (!value || typeof value !== 'object') return;
      for (const [key, child] of Object.entries(value)) {
        if (key.toLowerCase() === 'uri') fail('Reference meshes must be self-contained, with no external resource links.');
        visit(child);
      }
    }
    visit(gltf);
  }
  async function open(input) {
    if (!queries) fail('Cooked query scripts are unavailable. Reload the page and try again.');
    let bytes = new Uint8Array(input.arrayBuffer ? await input.arrayBuffer() : input);
    if (bytes[0] === 0x1f && bytes[1] === 0x8b) {
      if (typeof DecompressionStream === 'undefined') fail('This browser needs an uncompressed .json reference pack.');
      bytes = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
    }
    let pack;
    try { pack = JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(bytes)); }
    catch (_) { fail('This file is not a reference pack. Choose its .json or .json.gz export.'); }
    if (pack.format !== 'wardogs-cooked-reference-v1') fail('Unsupported reference pack format.');
    if (pack.build_sha256 !== BUILD) fail('This pack targets a different game build than the query model.');
    if (typeof pack.manifest_json !== 'string' || !pack.resources || !pack.glbs) fail('The reference pack is incomplete. Export it again.');
    await verified(encoder.encode(pack.manifest_json), pack.manifest_sha256, 'Reference manifest');
    let manifest;
    try { manifest = JSON.parse(pack.manifest_json); }
    catch (_) { fail('The reference manifest is invalid. Export the pack again.'); }
    const scenes = new Map(), buffers = new Map(), prepared = new Map(), models = new Map();
    if (!Array.isArray(manifest.scenes) || !manifest.scenes.length) fail('The pack contains no reference scenes.');
    for (const [sha, text] of Object.entries(pack.resources)) {
      if (typeof text !== 'string') fail('Invalid cooked resource.');
      await verified(encoder.encode(text), sha, 'Cooked resource');
    }
    for (const scene of manifest.scenes) {
      if (typeof scene.reference_model !== 'string' || scenes.has(scene.reference_model) || !scene.metadata || !Array.isArray(scene.native_components)) fail('Invalid reference model mapping.');
      const encoded = pack.glbs[scene.scene_sha256];
      if (typeof encoded !== 'string') fail('A reference collision mesh is missing.');
      if (!buffers.has(scene.scene_sha256)) {
        const data = decode(encoded);
        await verified(data, scene.scene_sha256, 'Reference collision mesh');
        selfContainedMesh(data);
        buffers.set(scene.scene_sha256, data);
      }
      for (const component of scene.native_components) {
        if (!component.query || !Array.isArray(component.query.resources) || component.query.resources.length !== 1) fail('Unsupported cooked component layout.');
        for (const resource of component.query.resources) {
          if (typeof pack.resources[resource.sha256] !== 'string') fail('A required cooked resource is missing.');
        }
      }
      scenes.set(scene.reference_model, scene);
    }
    let disposed = false;
    function resourceMesh(resource) {
      if (!prepared.has(resource.sha256)) {
        const data = JSON.parse(pack.resources[resource.sha256]);
        prepared.set(resource.sha256, data.complexImplicits.map(queries.prepareMesh));
      }
      const mesh = prepared.get(resource.sha256)[resource.implicit_index];
      if (!mesh || mesh.triangles.length !== resource.surface_slots.length) fail('Cooked face/material mapping is inconsistent.');
      return mesh;
    }
    return {
      modelCount: scenes.size,
      sceneFor(modelPath) {
        if (disposed) fail('This reference pack has been released.');
        const scene = scenes.get(modelPath);
        if (!scene) return null;
        if (!models.has(modelPath)) {
          const bytes = buffers.get(scene.scene_sha256);
          models.set(modelPath, {
            scene,
            url: URL.createObjectURL(new Blob([bytes], {type: 'model/gltf-binary'})),
            attach(geometry) {
              if (disposed) fail('This reference pack has been released.');
              return queries.attach(geometry, scene, resourceMesh);
            }
          });
        }
        return models.get(modelPath);
      },
      dispose() {
        models.forEach(model => URL.revokeObjectURL(model.url));
        models.clear(); prepared.clear(); buffers.clear(); disposed = true;
      }
    };
  }
  return {open};
}));
