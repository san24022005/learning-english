// Gọi đến API lấy toàn bộ lesson
fetch('/api/lessons')
  .then(response => {
    if (!response.ok) {
      throw new Error(`Lỗi kết nối đến server. Trạng thái: ${response.status}`);
    }
    return response.json();
  })
  .then(res => {
    if (!res.success) {
      console.error('API trả về lỗi:', res.error);
      return;
    }

    const lessonsList = res.data || [];
    const info = document.getElementById('info');
    const container = document.getElementById('lessons');
    const paginationContainer = document.getElementById('info__container');

    if (!container || !paginationContainer || !info) {
      console.error("Không tìm thấy phần tử cần thiết trên giao diện.");
      return;
    }

    const currentLevel = parseInt(info.dataset.level, 10) || 1;
    const perPage = 5;
    const totalLessons = lessonsList.length;
    const totalPages = Math.max(1, Math.ceil(totalLessons / perPage));
    let currentPage = Math.min(totalPages, Math.max(1, Math.ceil(currentLevel / perPage)));

    const renderLessons = page => {
      container.innerHTML = '';
      const startIndex = (page - 1) * perPage;
      const pageItems = lessonsList.slice(startIndex, startIndex + perPage);

      pageItems.forEach(lessonItem => {
        const lessonBlock = document.createElement('div');
        lessonBlock.className = 'lesson-block';
        lessonBlock.id = `lesson${lessonItem.lesson}`;

        const title = document.createElement('h3');
        title.textContent = `Lesson ${lessonItem.lesson}`;
        title.classList.add('lesson__title');

        if (lessonItem.lesson === currentLevel) {
          title.classList.add('lesson__title--active');
        }

        const lessonContainer = document.createElement('div');
        lessonContainer.classList.add('lesson__container');

        const lessonMain = document.createElement('div');
        lessonMain.classList.add('lesson__main');

        const wordsContainer = document.createElement('div');
        wordsContainer.className = 'lesson_words';

        const wordsArray = (lessonItem.questions || []).map(q => q.Word).filter(Boolean);
        if (wordsArray.length > 0) {
          wordsArray.forEach(wordText => {
            const wordDiv = document.createElement('div');
            wordDiv.className = 'lesson__word';
            wordDiv.textContent = wordText;
            wordsContainer.appendChild(wordDiv);
          });
        } else {
          wordsContainer.textContent = 'Không có từ vựng';
        }

        lessonBlock.appendChild(title);
        lessonBlock.appendChild(lessonContainer);
        lessonContainer.appendChild(wordsContainer);
        lessonContainer.appendChild(lessonMain);
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
    };

    const renderPagination = () => {
      paginationContainer.innerHTML = '';

      const prevButton = document.createElement('button');
      prevButton.type = 'button';
      prevButton.textContent = 'Quay lại';
      prevButton.disabled = currentPage <= 1;
      prevButton.className = 'pagination-button';
      prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
          currentPage -= 1;
          renderLessons(currentPage);
          renderPagination();
        }
      });

      const nextButton = document.createElement('button');
      nextButton.type = 'button';
      nextButton.textContent = 'Tiếp theo';
      nextButton.disabled = currentPage >= totalPages;
      nextButton.className = 'pagination-button';
      nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
          currentPage += 1;
          renderLessons(currentPage);
          renderPagination();
        }
      });

      const pageInfo = document.createElement('span');
      pageInfo.className = 'pagination-info';
      pageInfo.className = 'page__info'
      pageInfo.textContent = `Trang ${currentPage} / ${totalPages}`;

      paginationContainer.appendChild(prevButton);
      paginationContainer.appendChild(pageInfo);
      paginationContainer.appendChild(nextButton);
    };

    renderLessons(currentPage);
    renderPagination();
  })
  .catch(error => console.error('Lỗi khi fetch dữ liệu:', error));