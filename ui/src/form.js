import React from 'react';

import { Formik, Form, Field } from 'formik';

export default function AlertForm (props)  {
  return <div>
    <Formik
      initialValues={
          {n_msgs: 1000, monitor_rate: 5, fail_rate: 0.001, num_senders: 2, poll_rate: 1}
        }

      onSubmit={(values) => {
        fetch('/api/v1/register', {
            body: JSON.stringify(values),
            headers: {'content-type': 'application/json'},
            method: 'POST',
        }).then( (rsp) => {
            rsp.json().then( (data) => {
                console.log(data)
                props.setAlertId(data.id)
                props.setPollRate(values.poll_rate)
            })
        })
      }}
    >
      {() => (
        <Form>
          <div> Number of Messages to send</div>
          <Field name="n_msgs" test-id="msgs-field"/>
          <div> Failure Rate</div>
          <Field name="fail_rate" test-id="fail-rate-field"/>
          <div> Number of workers</div>
          <Field name="num_senders" test-id="n-senders-field"/>
          <div> Poll Rate</div>
          <Field name="poll_rate" test-id="poll-rate-field"/>
          <div> Submit the job to backend</div>
          <button type="submit" test-id= "test-form-submit">
            Submit
          </button>
        </Form>
      )}
    </Formik>
  </div>
};
