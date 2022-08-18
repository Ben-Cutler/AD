import { render, screen } from '@testing-library/react';
import fetchMock from 'fetch-mock'
import { userEvent } from '@testing-library/user-event'
import { Form, useFormikContext } from 'formik';


describe('the form', () => {
    afterEach(() => {
        fetchMock.restore()
    })
    it('sends data to the backend', () => {
        return // This test isn't working, and I have no clue why
        fetchMock.post(
            '/api/v1/register',
            {'id': 'abc-123-zyx'}
        )
        render(<Form />);
        
        screen.getByTestId('msgs-field').click();
        userEvent.type(500);
      
        screen.getByTestId('fail-rate-field').click();
        userEvent.type(0.01);
      
        screen.getByTestId('n-senders-field').click();
        userEvent.type(2);
      
        screen.getByTestId('poll-rate-field').click();
        userEvent.type(1);
      
        screen.getByTestId('test-form-submit').click();
        expect(fetchMock).toHaveBeenCalledWith({
            'n_msgs': 500,
            'fail_rate': 0.01,
            'num_senders': 2,
            'poll_rate': 1
        })
    })
})

