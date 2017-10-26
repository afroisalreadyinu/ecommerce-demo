import React from 'react';
import ReactDOM from 'react-dom';

import { fromJS } from 'immutable';

const initialState = fromJS({userEmail: null})

var h1 = React.createElement('h1', {}, 'Hello World');
ReactDOM.render(
  h1,
  document.getElementById('app')
);
