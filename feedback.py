import slither_runner
import chatgpt 

def feedback_loop(str user_prompt)

    for i in range(0,7):
        interation = get_chatgpt_response(user_prompt)
        feedback = run_slither_on_contract(str(interation))
        user_prompt = user_prompt + "edit based on the feedback from slither" + feedback
    
    return iteration

def main():
    prompt_example = "Generate an atomic transaction solidity smart contract that allows the user to book a hotel room and airplane ticket at a certain price limit at the same time"
    final_output = feedback_loop(prompt_example)
    print(final_output)


if __name__ == "__main__":
    main()