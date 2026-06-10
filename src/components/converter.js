// File Converter Application
class FileConverter {
    constructor() {
        this.selectedFile = null;
        this.recentConversions = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadRecentConversions();
    }

    setupEventListeners() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const removeFileBtn = document.getElementById('removeFile');
        const convertBtn = document.getElementById('convertBtn');
        const fromFormat = document.getElementById('fromFormat');
        const toFormat = document.getElementById('toFormat');

        // File upload events
        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        uploadArea.addEventListener('drop', (e) => this.handleDrop(e));

        fileInput.addEventListener('change', (e) => this.handleFileSelect(e.target.files[0]));
        removeFileBtn.addEventListener('click', () => this.removeFile());
        convertBtn.addEventListener('click', () => this.convertFile());

        // Enable convert button when both file and target format are selected
        toFormat.addEventListener('change', () => this.updateConvertButton());
        fromFormat.addEventListener('change', () => this.updateConvertButton());
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('uploadArea').style.transform = 'scale(1.05)';
        document.getElementById('uploadArea').style.borderColor = 'rgba(255, 255, 255, 0.8)';
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('uploadArea').style.transform = 'scale(1)';
        document.getElementById('uploadArea').style.borderColor = 'rgba(255, 255, 255, 0.4)';
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('uploadArea').style.transform = 'scale(1)';
        document.getElementById('uploadArea').style.borderColor = 'rgba(255, 255, 255, 0.4)';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFileSelect(files[0]);
        }
    }

    handleFileSelect(file) {
        if (!file) return;

        // Validate file size (max 100MB)
        const maxSize = 100 * 1024 * 1024;
        if (file.size > maxSize) {
            this.showStatus('File size exceeds 100MB limit', 'error');
            return;
        }

        this.selectedFile = file;
        this.updateFilePreview();
        this.autoDetectFormat();
        this.updateConvertButton();
    }

    updateFilePreview() {
        const uploadArea = document.getElementById('uploadArea');
        const filePreview = document.getElementById('filePreview');
        const fileName = document.getElementById('fileName');

        uploadArea.style.display = 'none';
        filePreview.style.display = 'block';
        fileName.textContent = `📄 ${this.selectedFile.name}`;
    }

    removeFile() {
        this.selectedFile = null;
        document.getElementById('uploadArea').style.display = 'block';
        document.getElementById('filePreview').style.display = 'none';
        document.getElementById('fileInput').value = '';
        document.getElementById('statusMessage').style.display = 'none';
        this.updateConvertButton();
    }

    autoDetectFormat() {
        const extension = this.selectedFile.name.split('.').pop().toLowerCase();
        const formatMap = {
            'pdf': 'pdf',
            'doc': 'doc',
            'docx': 'docx',
            'txt': 'txt',
            'png': 'png',
            'jpg': 'jpg',
            'jpeg': 'jpg',
            'xlsx': 'xlsx',
            'xls': 'xlsx',
            'csv': 'csv',
            'pptx': 'pptx',
            'ppt': 'pptx'
        };

        const format = formatMap[extension] || '';
        document.getElementById('fromFormat').value = format;
    }

    updateConvertButton() {
        const convertBtn = document.getElementById('convertBtn');
        const hasFile = this.selectedFile !== null;
        const hasToFormat = document.getElementById('toFormat').value !== '';
        convertBtn.disabled = !(hasFile && hasToFormat);
    }

    async convertFile() {
        const toFormat = document.getElementById('toFormat').value;
        const fromFormat = document.getElementById('fromFormat').value;

        if (!this.selectedFile || !toFormat) {
            this.showStatus('Please select a file and output format', 'error');
            return;
        }

        this.showProgress();
        const convertBtn = document.getElementById('convertBtn');
        convertBtn.disabled = true;

        try {
            const conversionName = `${this.selectedFile.name.split('.')[0]}.${toFormat}`;
            console.log('Starting conversion:', {
                file: this.selectedFile.name,
                size: this.selectedFile.size,
                toFormat: toFormat,
                fromFormat: fromFormat
            });

            // Send file to backend for conversion
            const formData = new FormData();
            formData.append('file', this.selectedFile);
            formData.append('to_format', toFormat);
            if (fromFormat) {
                formData.append('from_format', fromFormat);
            }

            console.log('FormData prepared, sending to /api/convert');

            // Call backend API
            const response = await fetch('/api/convert', {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const contentType = response.headers.get('content-type');
                let error = { error: `HTTP ${response.status}` };

                if (contentType && contentType.includes('application/json')) {
                    error = await response.json();
                } else {
                    const text = await response.text();
                    error = { error: text || `HTTP ${response.status}` };
                }

                console.error('Conversion error:', error);
                throw new Error(error.error || 'Conversion failed');
            }

            // Download file from response
            const blob = await response.blob();
            console.log('Received blob:', blob.size, 'bytes');

            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = conversionName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);

            this.showStatus(`✓ Conversion successful! Downloaded: ${conversionName}`, 'success');
            this.addRecentConversion(this.selectedFile.name, toFormat);
            this.removeFile();
        } catch (error) {
            console.error('Catch error:', error);
            this.showStatus(`✗ Conversion failed: ${error.message}`, 'error');
        } finally {
            this.hideProgress();
            convertBtn.disabled = false;
        }
    }

    simulateConversion() {
        return new Promise((resolve) => {
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 25;
                if (progress >= 95) {
                    progress = 95; // Stop at 95% until actual completion
                }
                progressFill.style.width = progress + '%';
                progressText.textContent = `Converting... ${Math.floor(progress)}%`;

                if (progress >= 95) {
                    clearInterval(interval);
                    setTimeout(resolve, 300);
                }
            }, 150);
        });
    }

    completeProgress() {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        progressFill.style.width = '100%';
        progressText.textContent = 'Converting... 100%';
    }

    showProgress() {
        const progressContainer = document.getElementById('progressContainer');
        progressContainer.style.display = 'block';
        document.getElementById('progressFill').style.width = '0%';
        document.getElementById('progressText').textContent = 'Converting... 0%';
    }

    hideProgress() {
        this.completeProgress();
        setTimeout(() => {
            document.getElementById('progressContainer').style.display = 'none';
        }, 1000);
    }

    showStatus(message, type) {
        const statusMessage = document.getElementById('statusMessage');
        statusMessage.textContent = message;
        statusMessage.className = `status-message ${type}`;
        statusMessage.style.display = 'block';

        if (type !== 'error') {
            setTimeout(() => {
                statusMessage.style.display = 'none';
            }, 3000);
        }
    }

    addRecentConversion(fromFile, toFormat) {
        const conversion = {
            fromFile: fromFile,
            toFormat: toFormat,
            timestamp: new Date().toLocaleTimeString()
        };
        this.recentConversions.unshift(conversion);
        if (this.recentConversions.length > 5) {
            this.recentConversions.pop();
        }
        this.saveRecentConversions();
        this.updateRecentList();
    }

    updateRecentList() {
        const recentList = document.getElementById('recentList');
        if (this.recentConversions.length === 0) {
            recentList.innerHTML = '<p class="empty-state">No conversions yet</p>';
            return;
        }

        recentList.innerHTML = this.recentConversions.map((conv, index) => `
            <div class="recent-item" style="animation: slideDown 0.3s ease ${index * 0.1}s both;">
                <div>
                    <strong>${conv.fromFile}</strong>
                    <p style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); margin-top: 5px;">
                        → ${conv.toFormat.toUpperCase()} • ${conv.timestamp}
                    </p>
                </div>
                <button class="btn-remove" onclick="converter.removeRecentItem(${index})">Delete</button>
            </div>
        `).join('');
    }

    removeRecentItem(index) {
        this.recentConversions.splice(index, 1);
        this.saveRecentConversions();
        this.updateRecentList();
    }

    saveRecentConversions() {
        localStorage.setItem('recentConversions', JSON.stringify(this.recentConversions));
    }

    loadRecentConversions() {
        const saved = localStorage.getItem('recentConversions');
        if (saved) {
            this.recentConversions = JSON.parse(saved);
            this.updateRecentList();
        }
    }
}

// Initialize the converter app
const converter = new FileConverter();
