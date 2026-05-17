import { useState } from "react";

const TAB = { SETUP: "setup", BASIC: "basic", TREE: "tree", QUERIES: "queries" };

const CODE = `% ============================================================
%  PROLOG FAMILY TREE — The Anderson Family
% ============================================================

% --- FACTS: parent(Parent, Child) ---
parent(george_anderson, david_anderson).
parent(george_anderson, susan_anderson).
parent(mary_anderson,  david_anderson).
parent(mary_anderson,  susan_anderson).

parent(harold_baker,   linda_baker).
parent(harold_baker,   robert_baker).
parent(dorothy_baker,  linda_baker).
parent(dorothy_baker,  robert_baker).

parent(david_anderson, emma_anderson).
parent(david_anderson, james_anderson).
parent(linda_baker,    emma_anderson).
parent(linda_baker,    james_anderson).

parent(robert_baker,   sophie_baker).
parent(robert_baker,   tom_baker).
parent(susan_anderson, sophie_baker).
parent(susan_anderson, tom_baker).

parent(emma_anderson,  lily_anderson).
parent(emma_anderson,  noah_anderson).
parent(james_anderson, oliver_anderson).

% --- FACTS: gender ---
male(george_anderson). male(harold_baker).
male(david_anderson).  male(robert_baker).
male(james_anderson).  male(tom_baker).
male(noah_anderson).   male(oliver_anderson).

female(mary_anderson).   female(dorothy_baker).
female(susan_anderson).  female(linda_baker).
female(emma_anderson).   female(sophie_baker).
female(lily_anderson).

% --- RULES ---
father(F,C)       :- parent(F,C), male(F).
mother(M,C)       :- parent(M,C), female(M).
grandparent(GP,GC):- parent(GP,P), parent(P,GC).
grandfather(GF,GC):- grandparent(GF,GC), male(GF).
grandmother(GM,GC):- grandparent(GM,GC), female(GM).
grandchild(GC,GP) :- grandparent(GP,GC).
sibling(X,Y)      :- parent(P,X), parent(P,Y), X\\=Y.
brother(X,Y)      :- sibling(X,Y), male(X).
sister(X,Y)       :- sibling(X,Y), female(X).
uncle(U,C)        :- parent(P,C), brother(U,P).
aunt(A,C)         :- parent(P,C), sister(A,P).
cousin(X,Y)       :- parent(PX,X), parent(PY,Y), sibling(PX,PY).
ancestor(A,D)     :- parent(A,D).
ancestor(A,D)     :- parent(A,X), ancestor(X,D).
descendant(D,A)   :- ancestor(A,D).`;

const QUERIES = [
  { q: "grandparent(george_anderson, X).", result: "X = emma_anderson\nX = james_anderson\nX = sophie_baker\nX = tom_baker", label: "Who are George's grandchildren?" },
  { q: "grandmother(mary_anderson, X).", result: "X = emma_anderson\nX = james_anderson\nX = sophie_baker\nX = tom_baker", label: "Mary's grandchildren" },
  { q: "uncle(U, sophie_baker).", result: "U = david_anderson\nU = robert_baker (fails – robert is father)\n→ U = david_anderson", label: "Sophie's uncle" },
  { q: "aunt(A, james_anderson).", result: "A = susan_anderson", label: "James's aunt" },
  { q: "cousin(X, Y).", result: "X = emma_anderson, Y = sophie_baker\nX = emma_anderson, Y = tom_baker\nX = james_anderson, Y = sophie_baker\n...", label: "All cousin pairs" },
  { q: "ancestor(george_anderson, lily_anderson).", result: "true", label: "Is George ancestor of Lily?" },
  { q: "descendant(X, george_anderson).", result: "X = david_anderson ; X = susan_anderson ;\nX = emma_anderson ; X = james_anderson ;\nX = sophie_baker ; X = tom_baker ;\nX = lily_anderson ; X = noah_anderson ;\nX = oliver_anderson", label: "All of George's descendants" },
  { q: "sibling(david_anderson, susan_anderson).", result: "true", label: "Are David and Susan siblings?" },
];

const FAMILY = {
  generations: [
    { label: "Grandparents", color: "#7c3aed", members: [
      { name: "George Anderson", id: "george_anderson", gender: "M" },
      { name: "Mary Anderson", id: "mary_anderson", gender: "F" },
      { name: "Harold Baker", id: "harold_baker", gender: "M" },
      { name: "Dorothy Baker", id: "dorothy_baker", gender: "F" },
    ]},
    { label: "Parents", color: "#0369a1", members: [
      { name: "David Anderson", id: "david_anderson", gender: "M" },
      { name: "Linda Baker", id: "linda_baker", gender: "F", note: "↕ married" },
      { name: "Susan Anderson", id: "susan_anderson", gender: "F" },
      { name: "Robert Baker", id: "robert_baker", gender: "M", note: "↕ married" },
    ]},
    { label: "Children", color: "#0f766e", members: [
      { name: "Emma Anderson", id: "emma_anderson", gender: "F" },
      { name: "James Anderson", id: "james_anderson", gender: "M" },
      { name: "Sophie Baker", id: "sophie_baker", gender: "F" },
      { name: "Tom Baker", id: "tom_baker", gender: "M" },
    ]},
    { label: "Grandchildren", color: "#b45309", members: [
      { name: "Lily Anderson", id: "lily_anderson", gender: "F" },
      { name: "Noah Anderson", id: "noah_anderson", gender: "M" },
      { name: "Oliver Anderson", id: "oliver_anderson", gender: "M" },
    ]},
  ]
};

const SETUP_STEPS = [
  {
    title: "Download SWI-Prolog",
    icon: "⬇️",
    steps: [
      "Go to https://www.swi-prolog.org/Download.html",
      "Choose your OS (Windows / macOS / Linux)",
      "Windows: run the .exe installer — accept defaults",
      "macOS: drag SWI-Prolog.app to /Applications",
      "Ubuntu/Debian: sudo apt-get install swi-prolog",
    ]
  },
  {
    title: "Verify Installation",
    icon: "✅",
    steps: [
      "Open a terminal (or SWI-Prolog app on Windows/Mac)",
      "Type: swipl",
      "You should see the ?- prompt",
      "Type: halt.  (to exit)",
    ],
    code: "$ swipl\nWelcome to SWI-Prolog (version ...)\n?- halt.\n$"
  },
  {
    title: "Load a .pl File",
    icon: "📂",
    steps: [
      "Save your Prolog file as family_tree.pl",
      "In the SWI-Prolog console, type:",
    ],
    code: "?- [family_tree].   % loads family_tree.pl\n% or\n?- consult('family_tree.pl').\n% You should see: true."
  },
  {
    title: "VS Code Integration (optional)",
    icon: "🖥️",
    steps: [
      "Install VS Code extension: 'VSC-Prolog'",
      "Enables syntax highlighting and inline query execution",
      "Right-click → 'Load into Prolog' runs the file",
    ]
  }
];

const BASIC_PROGRAMS = [
  {
    title: "Hello World",
    code: `% hello.pl
:- initialization(main, main).
main :- write('Hello from Prolog!'), nl.`,
    query: "?- main.",
    result: "Hello from Prolog!"
  },
  {
    title: "Simple Facts",
    code: `% facts.pl
likes(mary, food).
likes(mary, wine).
likes(john, wine).
likes(john, mary).`,
    query: "?- likes(mary, X).",
    result: "X = food ;\nX = wine"
  },
  {
    title: "Basic Rules",
    code: `% rules.pl
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).

grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).`,
    query: "?- grandparent(tom, Who).",
    result: "Who = ann"
  },
  {
    title: "Arithmetic",
    code: `% math.pl
square(X, Y) :- Y is X * X.
factorial(0, 1) :- !.
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.`,
    query: "?- square(5, Y).\n?- factorial(5, F).",
    result: "Y = 25\nF = 120"
  }
];

function CopyBtn({ text }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };
  return (
    <button onClick={copy} style={{
      position:"absolute", top:8, right:8,
      background: copied ? "#16a34a" : "#374151",
      color:"#fff", border:"none", borderRadius:4,
      padding:"3px 10px", fontSize:11, cursor:"pointer",
      fontFamily:"monospace", transition:"background 0.2s"
    }}>{copied ? "✓ Copied" : "Copy"}</button>
  );
}

function CodeBlock({ code, style={} }) {
  return (
    <div style={{ position:"relative", ...style }}>
      <pre style={{
        background:"#0f172a", color:"#e2e8f0",
        borderRadius:8, padding:"14px 44px 14px 14px",
        fontSize:12, lineHeight:1.7, overflowX:"auto",
        margin:0, fontFamily:"'Fira Code', 'Courier New', monospace",
        border:"1px solid #1e293b"
      }}>{code}</pre>
      <CopyBtn text={code} />
    </div>
  );
}

export default function App() {
  const [tab, setTab] = useState(TAB.SETUP);
  const [activeQuery, setActiveQuery] = useState(null);

  const tabs = [
    { id: TAB.SETUP,   label: "① Setup" },
    { id: TAB.BASIC,   label: "② Basic Programs" },
    { id: TAB.TREE,    label: "③ Family Tree" },
    { id: TAB.QUERIES, label: "④ Query Tester" },
  ];

  return (
    <div style={{
      minHeight:"100vh",
      background:"linear-gradient(135deg, #0a0a1a 0%, #0f1629 50%, #0a1a0f 100%)",
      color:"#e2e8f0", fontFamily:"'Segoe UI', system-ui, sans-serif",
      padding:"0 0 40px"
    }}>
      {/* Header */}
      <div style={{
        background:"linear-gradient(90deg, #1e1b4b, #0c1a3a, #052e16)",
        borderBottom:"2px solid #312e81",
        padding:"28px 32px 20px"
      }}>
        <div style={{ maxWidth:900, margin:"0 auto" }}>
          <div style={{ display:"flex", alignItems:"center", gap:12, marginBottom:6 }}>
            <span style={{ fontSize:32 }}>🧠</span>
            <h1 style={{
              margin:0, fontSize:26, fontWeight:800, letterSpacing:-0.5,
              background:"linear-gradient(90deg, #a78bfa, #67e8f9, #6ee7b7)",
              WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent"
            }}>Prolog Lab — Task Three</h1>
          </div>
          <p style={{ margin:0, color:"#94a3b8", fontSize:14 }}>
            Download · Configure · Basic Programs · Custom Family Tree
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        display:"flex", gap:4, padding:"16px 32px 0",
        maxWidth:900, margin:"0 auto", flexWrap:"wrap"
      }}>
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{
            padding:"9px 20px", borderRadius:"8px 8px 0 0",
            border:"1px solid " + (tab===t.id ? "#6366f1" : "#1e293b"),
            borderBottom: tab===t.id ? "2px solid #0f172a" : "1px solid #1e293b",
            background: tab===t.id ? "#1e1b4b" : "#0f172a",
            color: tab===t.id ? "#a78bfa" : "#64748b",
            fontWeight: tab===t.id ? 700 : 400,
            fontSize:13, cursor:"pointer", transition:"all 0.15s"
          }}>{t.label}</button>
        ))}
      </div>

      {/* Content */}
      <div style={{
        maxWidth:900, margin:"0 auto", padding:"0 32px",
        background:"#0f172a", border:"1px solid #1e293b",
        borderRadius:"0 8px 8px 8px", minHeight:500
      }}>

        {/* ── SETUP ── */}
        {tab === TAB.SETUP && (
          <div style={{ padding:"28px 0" }}>
            <h2 style={{ color:"#a78bfa", marginTop:0 }}>Part (a) — Download & Configure SWI-Prolog</h2>
            <div style={{ display:"grid", gap:16 }}>
              {SETUP_STEPS.map((s, i) => (
                <div key={i} style={{
                  background:"#1e293b", borderRadius:10,
                  border:"1px solid #334155", padding:"18px 20px"
                }}>
                  <h3 style={{ margin:"0 0 12px", color:"#67e8f9", fontSize:15 }}>
                    {s.icon} Step {i+1}: {s.title}
                  </h3>
                  <ul style={{ margin:"0 0 12px", paddingLeft:20 }}>
                    {s.steps.map((st, j) => (
                      <li key={j} style={{ color:"#cbd5e1", fontSize:13, marginBottom:4 }}>{st}</li>
                    ))}
                  </ul>
                  {s.code && <CodeBlock code={s.code} />}
                </div>
              ))}
            </div>
            <div style={{
              marginTop:20, background:"#052e16", border:"1px solid #166534",
              borderRadius:8, padding:"14px 18px"
            }}>
              <strong style={{ color:"#4ade80" }}>💡 Tip:</strong>
              <span style={{ color:"#a7f3d0", fontSize:13 }}> SWI-Prolog is free, open-source and runs on all platforms. The interactive console (REPL) is all you need for this task.</span>
            </div>
          </div>
        )}

        {/* ── BASIC PROGRAMS ── */}
        {tab === TAB.BASIC && (
          <div style={{ padding:"28px 0" }}>
            <h2 style={{ color:"#a78bfa", marginTop:0 }}>Part (b) — Basic Prolog Programs</h2>
            <p style={{ color:"#94a3b8", fontSize:13, marginTop:0 }}>
              Run these in SWI-Prolog to verify your installation and learn the basics.
            </p>
            <div style={{ display:"grid", gap:20 }}>
              {BASIC_PROGRAMS.map((p, i) => (
                <div key={i} style={{
                  background:"#1e293b", borderRadius:10,
                  border:"1px solid #334155", padding:"18px 20px"
                }}>
                  <h3 style={{ margin:"0 0 12px", color:"#67e8f9", fontSize:15 }}>
                    {i+1}. {p.title}
                  </h3>
                  <div style={{ marginBottom:10 }}>
                    <div style={{ color:"#94a3b8", fontSize:11, marginBottom:4 }}>CODE:</div>
                    <CodeBlock code={p.code} />
                  </div>
                  <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10 }}>
                    <div>
                      <div style={{ color:"#94a3b8", fontSize:11, marginBottom:4 }}>QUERY:</div>
                      <CodeBlock code={p.query} />
                    </div>
                    <div>
                      <div style={{ color:"#94a3b8", fontSize:11, marginBottom:4 }}>OUTPUT:</div>
                      <pre style={{
                        background:"#0f2d1a", color:"#4ade80",
                        borderRadius:8, padding:"10px 14px",
                        fontSize:12, margin:0, border:"1px solid #166534",
                        fontFamily:"monospace"
                      }}>{p.result}</pre>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── FAMILY TREE ── */}
        {tab === TAB.TREE && (
          <div style={{ padding:"28px 0" }}>
            <h2 style={{ color:"#a78bfa", marginTop:0 }}>Part (c) — The Anderson Family Tree</h2>
            <p style={{ color:"#94a3b8", fontSize:13, marginTop:0 }}>
              A complete family with 4 generations, cousins, aunts, and uncles.
            </p>

            {/* Visual Tree */}
            <div style={{
              background:"#1e293b", borderRadius:10, border:"1px solid #334155",
              padding:"20px", marginBottom:20, overflowX:"auto"
            }}>
              {FAMILY.generations.map((gen, gi) => (
                <div key={gi} style={{ marginBottom: gi < FAMILY.generations.length-1 ? 16 : 0 }}>
                  <div style={{
                    fontSize:11, color:"#94a3b8", fontWeight:700,
                    textTransform:"uppercase", letterSpacing:1,
                    marginBottom:8
                  }}>{gen.label}</div>
                  <div style={{ display:"flex", flexWrap:"wrap", gap:8 }}>
                    {gen.members.map((m, mi) => (
                      <div key={mi} style={{
                        background: gen.color + "22",
                        border:"1.5px solid " + gen.color + "88",
                        borderRadius:8, padding:"8px 14px",
                        fontSize:13, color:"#e2e8f0",
                        display:"flex", alignItems:"center", gap:6
                      }}>
                        <span>{m.gender === "M" ? "👨" : "👩"}</span>
                        <div>
                          <div style={{ fontWeight:600 }}>{m.name}</div>
                          <div style={{ fontSize:10, color:"#64748b", fontFamily:"monospace" }}>{m.id}</div>
                          {m.note && <div style={{ fontSize:10, color: gen.color }}>{m.note}</div>}
                        </div>
                      </div>
                    ))}
                  </div>
                  {gi < FAMILY.generations.length-1 && (
                    <div style={{ color:"#334155", fontSize:18, marginTop:8, paddingLeft:20 }}>↓</div>
                  )}
                </div>
              ))}
            </div>

            {/* Relationships legend */}
            <div style={{
              display:"grid", gridTemplateColumns:"1fr 1fr", gap:12, marginBottom:20
            }}>
              {[
                { rel:"Siblings", value:"David & Susan Anderson; Robert & Linda Baker (parents only)" },
                { rel:"Cousins", value:"Emma & James ↔ Sophie & Tom (children generation)" },
                { rel:"Uncle", value:"David Anderson is uncle to Sophie & Tom Baker" },
                { rel:"Aunt", value:"Susan Anderson is aunt to Emma & James Anderson" },
                { rel:"Grandchildren", value:"Lily, Noah (via Emma); Oliver (via James)" },
                { rel:"Grandparents", value:"George & Mary Anderson; Harold & Dorothy Baker" },
              ].map((r, i) => (
                <div key={i} style={{
                  background:"#0f172a", borderRadius:8, padding:"10px 14px",
                  border:"1px solid #1e293b"
                }}>
                  <div style={{ color:"#67e8f9", fontSize:12, fontWeight:700 }}>{r.rel}</div>
                  <div style={{ color:"#94a3b8", fontSize:12 }}>{r.value}</div>
                </div>
              ))}
            </div>

            {/* Full code */}
            <div style={{ color:"#94a3b8", fontSize:12, marginBottom:8 }}>
              📄 Full <code style={{ color:"#a78bfa" }}>family_tree.pl</code> source:
            </div>
            <CodeBlock code={CODE} />
          </div>
        )}

        {/* ── QUERIES ── */}
        {tab === TAB.QUERIES && (
          <div style={{ padding:"28px 0" }}>
            <h2 style={{ color:"#a78bfa", marginTop:0 }}>Part (c) — Sample Queries & Results</h2>
            <p style={{ color:"#94a3b8", fontSize:13, marginTop:0 }}>
              Click any query to see the expected Prolog output.
            </p>
            <div style={{ display:"grid", gap:10 }}>
              {QUERIES.map((q, i) => (
                <div key={i}
                  onClick={() => setActiveQuery(activeQuery === i ? null : i)}
                  style={{
                    background: activeQuery===i ? "#1e1b4b" : "#1e293b",
                    border:"1.5px solid " + (activeQuery===i ? "#6366f1" : "#334155"),
                    borderRadius:8, padding:"14px 18px", cursor:"pointer",
                    transition:"all 0.15s"
                  }}
                >
                  <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
                    <div>
                      <span style={{ color:"#94a3b8", fontSize:11 }}>{q.label}</span>
                      <pre style={{
                        margin:"4px 0 0", color:"#67e8f9",
                        fontFamily:"monospace", fontSize:13
                      }}>?- {q.q}</pre>
                    </div>
                    <span style={{ color:"#475569", fontSize:18 }}>
                      {activeQuery===i ? "▲" : "▼"}
                    </span>
                  </div>
                  {activeQuery===i && (
                    <div style={{ marginTop:12, borderTop:"1px solid #334155", paddingTop:12 }}>
                      <div style={{ fontSize:11, color:"#94a3b8", marginBottom:6 }}>OUTPUT:</div>
                      <pre style={{
                        background:"#0f2d1a", color:"#4ade80",
                        borderRadius:6, padding:"10px 14px",
                        fontSize:12, margin:0, border:"1px solid #166534",
                        fontFamily:"monospace", whiteSpace:"pre-wrap"
                      }}>{q.result}</pre>
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div style={{
              marginTop:24, background:"#1c1400", border:"1px solid #78350f",
              borderRadius:8, padding:"14px 18px"
            }}>
              <strong style={{ color:"#fbbf24" }}>📌 How to load and run:</strong>
              <CodeBlock code={`$ swipl\n?- [family_tree].        % load the file\n% true.\n?- grandparent(george_anderson, X).\n% X = emma_anderson ;\n% X = james_anderson ; ...\n?- cousin(X, Y).\n?- halt.                  % exit`}
                style={{ marginTop:10 }} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
