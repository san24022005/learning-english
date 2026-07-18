// Gọi đến API lấy toàn bộ lesson
fetch('/api/lessons') 
  .then(response => {
    if (!response.ok) {
      throw new Error(`Lỗi kết nối đến server. Trạng thái: ${response.status}`);
    }
    return response.json();
  })
  .then(res => {
    if (res.success) {
      const container = document.getElementById('lessons');
      
      if (!container) {
          console.error("Không tìm thấy phần tử 'lessons' trên giao diện.");
          return;
      }

      const lessonsList = res.data || [];
      
      lessonsList.forEach(lessonItem => {
        
        // 1. Tạo block chứa cho mỗi lesson
        const lessonBlock = document.createElement('div');
        lessonBlock.className = 'lesson-block';

        // 2. Tạo tiêu đề Lesson
        const title = document.createElement('h3');
        title.textContent = `Lesson ${lessonItem.lesson}`;
        title.classList.add('lesson__title')

        const lessonContainer = document.createElement('div');
        lessonContainer.classList.add('lesson__container')

        const lessonMain = document.createElement('div')
        lessonMain.classList.add('lesson__main')


        // 3. Tạo container 'lesson_words' để chứa các thẻ word bên trong
        const wordsContainer = document.createElement('div');
        wordsContainer.className = 'lesson_words'; // Bạn có thể sửa thành 'lesson__words' nếu muốn chuẩn BEM hoàn toàn

        // Lấy ra danh sách các Word hợp lệ
        const wordsArray = (lessonItem.questions || []).map(q => q.Word).filter(Boolean);
        
        if (wordsArray.length > 0) {
          wordsArray.forEach(wordText => {
            // Tạo thẻ div cho từng từ vựng với class 'lesson__word'
            const wordDiv = document.createElement('div');
            wordDiv.className = 'lesson__word';
            wordDiv.textContent = wordText;
            
            // Bỏ thẻ word vào trong container chứa tổng
            wordsContainer.appendChild(wordDiv);
          });
        } else {
          // Trường hợp bài học không có câu hỏi/từ vựng nào
          wordsContainer.textContent = 'Không có từ vựng';
        }

        // 4. Gắn các phần tử vào DOM
        lessonBlock.appendChild(title);
        lessonBlock.appendChild(lessonContainer);
        lessonContainer.appendChild(wordsContainer)
        lessonContainer.appendChild(lessonMain)
        container.appendChild(lessonBlock);

        title.addEventListener('click', () => {

            document.querySelectorAll('.lesson__container').forEach(item => {
                if (item !== lessonContainer) {
                    item.classList.remove('active');
                }
            });

            lessonContainer.classList.toggle('active');
        });
      });
    } else {
      console.error('API trả về lỗi:', res.error);
    }
  })
  .catch(error => console.error('Lỗi khi fetch dữ liệu:', error));