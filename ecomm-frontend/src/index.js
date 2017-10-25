import React from 'react';
import ReactDOM from 'react-dom';

var h1 = React.createElement('h1', {}, 'Hello World');
ReactDOM.render(
  h1,
  document.getElementById('app')
);
