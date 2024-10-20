import React from 'react';
import Weather from './container/WebApp';

function App() {
  return (
    <div className="App">
      <h1 style={{textAlign: "center",
    fontFamily: "Helvetica",
    color: "#555555"}}>Weather App</h1>
      <Weather />
    </div>
  );
}

export default App;
