document.addEventListener('DOMContentLoaded', () => {   
  const chatWindow = document.getElementById('chat-window');
  const inputField = document.getElementById('input');
  const sendButton = document.getElementById('send');

  const addMessageToChat = (message, sender) => {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container', sender);

    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerText = message;

    const avatar = document.createElement('img');
    avatar.classList.add('avatar');
    avatar.src = sender === 'user' ? 'user-avatar.png' : 'bot-avatar.png';

    messageContainer.appendChild(avatar);
    messageContainer.appendChild(messageElement);
    
    chatWindow.appendChild(messageContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  };

  const getBotResponse = async (userMessage) => {                 
    const response = await fetch('http://127.0.0.1:1954/HUFS', {   
      method: 'POST',                                             
      headers: { 'Content-Type': 'application/json' },           
      body: JSON.stringify({ message: userMessage })        
    });
    const data = await response.json();     
    return data.response;           
  };

  addMessageToChat("안녕하세요!\n<채찍피티> 팀에서 제작한 2023-1학기 수강편람 챗봇입니다.\n사용 방법은 다음과 같습니다:\n 1. 질문하기: 한국외국어대학교의 수강 신청, 졸업 요건, 전공, 교과목 등에 관한 질문을 자유롭게 입력하세요.\n2. 정보 범위: 수강신청 일정, 졸업 이수학점, 교과영역, 학사제도, 교직과정, 전공 필수 과목, 수강 금지 교과목 등 다양한 학사 정보를 제공합니다.\n3. 구체적인 질문: 더 정확한 답변을 받기 위해 가능한 한 구체적으로 질문해주세요. 예를 들어, 학과명, 학번, 특정 과목명 등을 포함하면 좋습니다.\n4. 페이지 참조: 답변 끝에 '관련 페이지' 정보가 제공되며, 이를 통해 원본 자료의 위치를 확인할 수 있습니다.\n6. 기타: 수강편람 정보 외의 질문에는 '그 질문에 대한 답은 드릴 수 없습니다.'라고 답변할 수 있습니다.\n궁금한 점이 있으면 언제든 물어보세요!", 'bot');

  sendButton.addEventListener('click', async () => {     
    const userMessage = inputField.value;                 
    if (userMessage) {
      addMessageToChat(userMessage, 'user');           
      inputField.value = '';                   

      const botResponse = await getBotResponse(userMessage);
      addMessageToChat(botResponse, 'bot');         
    }
  });

  inputField.addEventListener('keypress', (event) => {  
    if (event.key === 'Enter') {
      sendButton.click();
    }
  });
});
