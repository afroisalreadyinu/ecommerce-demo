import React from 'react';
import ReactDOM from 'react-dom';
import { createStore } from 'redux'
import { Provider } from 'react-redux'
import PropTypes from 'prop-types'
import { fromJS } from 'immutable';

const initialState = fromJS({userEmail: null});

// Reducer

function ecommerceReducer(state=initialState, action) {
  switch(action.type) {
  case 'LOGIN':
    return Object.assign({}, state, {email: action.email});
  default:
    return initialState;
  };
};

// Components

const SetEmail = ({ onSubmit }) => (
  <form onSubmit={onSubmit} >
    <input placeholder="Email"></input>
    <input type="submit" value="Set"></input>
  </form>
)

SetEmail.propTypes = {
  onSubmit: PropTypes.func.isRequired,
}

function setEmail() {
  console.log("Something happened");
}

const VisibleSetEmail = connect(
  state => state.userEmail,
  mapDispatchToProps
)(SetEmail)

const App = () => (
  <div>
    <SetEmail onSubmit={setEmail}/>
  </div>
)

let store = createStore(ecommerceReducer);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('app')
);
