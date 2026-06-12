const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// regex to move 🚧 to the start of the a tag
const regex = /(<a class="sidebar-link"[^>]*>)(.*?)(<span class="sidebar-id">.*?<\/span>)\s*🚧\s*(<\/a>)/g;
html = html.replace(regex, '$1🚧 $2 $3$4');

// Now re-insert the 04.4.4 link if it's missing
if (!html.includes('04.4.4-relacion-depositos.html')) {
    html = html.replace(
        '<a class="sidebar-link" target="contentFrame" href="04_ingresos/04.4.3-recibos.html">Recibos Oficiales <span class="sidebar-id">04.4.3</span> 🚧</a>',
        '<a class="sidebar-link" target="contentFrame" href="04_ingresos/04.4.3-recibos.html">Recibos Oficiales <span class="sidebar-id">04.4.3</span> 🚧</a>\n        <a class="sidebar-link" target="contentFrame" href="04_ingresos/04.4.4-relacion-depositos.html">Relación de Depósitos <span class="sidebar-id">04.4.4</span></a>'
    );
    // Also try the replaced version in case the 🚧 was already moved
    html = html.replace(
        '<a class="sidebar-link" target="contentFrame" href="04_ingresos/04.4.3-recibos.html">🚧 Recibos Oficiales <span class="sidebar-id">04.4.3</span></a>',
        '<a class="sidebar-link" target="contentFrame" href="04_ingresos/04.4.3-recibos.html">🚧 Recibos Oficiales <span class="sidebar-id">04.4.3</span></a>\n        <a class="sidebar-link" target="contentFrame" href="04_ingresos/04.4.4-relacion-depositos.html">Relación de Depósitos <span class="sidebar-id">04.4.4</span></a>'
    );
}

fs.writeFileSync('index.html', html, 'utf8');
console.log("Updated index.html successfully.");
