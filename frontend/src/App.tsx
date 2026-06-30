export default function App(){
return (
<div style={{maxWidth:900,margin:"auto",padding:40,fontFamily:"sans-serif"}}>
<h1>📰 NewsVerifier AI</h1>
<p>Powered by GenLayer Intelligent Contracts</p>
<input style={{width:"80%",padding:12}} placeholder="https://news.example/article"/>
<button style={{padding:12,marginLeft:10}}>Verify</button>
<hr/>
<h2>Verdict</h2>
<div>Awaiting verification...</div>
</div>
)}
