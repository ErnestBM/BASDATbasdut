CREATE OR REPLACE FUNCTION validate_pelatih_count()
RETURNS TRIGGER AS $$
DECLARE
    pelatih_count INTEGER;
BEGIN
    -- Menghitung jumlah pelatih yang sudah terdaftar pada tim
    SELECT COUNT(*) INTO pelatih_count
    FROM Pelatih
    WHERE nama_tim = NEW.nama_tim;
    
    IF pelatih_count = 0 THEN
        -- Jika belum ada pelatih, langsung dapat mendaftarkan pelatih baru
        RETURN NEW;
    ELSIF pelatih_count = 1 THEN
        -- Jika sudah ada satu pelatih, periksa spesialisasi pelatih baru
        SELECT COUNT(*) INTO pelatih_count
        FROM Spesialisasi_Pelatih
        WHERE id_pelatih = NEW.id_pelatih
        AND id_pelatih IN (
            SELECT id_pelatih
            FROM Pelatih
            WHERE nama_tim = NEW.nama_tim
        );
        
        IF pelatih_count = 0 THEN
            -- Jika spesialisasi pelatih baru berbeda, daftarkan pelatih baru
            RETURN NEW;
        ELSE
            -- Jika spesialisasi pelatih baru sama, kirimkan pesan error
            RAISE EXCEPTION 'Pelatih dengan spesialisasi yang sama sudah terdaftar pada tim.';
        END IF;
    ELSE
        -- Jika sudah ada dua pelatih, kirimkan pesan error
        RAISE EXCEPTION 'Tim sudah memiliki dua pelatih.';
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_kapten()
RETURNS TRIGGER AS $$
BEGIN
    -- Menghapus kapten lama
    UPDATE Pemain
    SET is_captain = FALSE
    WHERE nama_tim = NEW.nama_tim;
    
    -- Menetapkan pemain baru sebagai kapten
    UPDATE Pemain
    SET is_captain = TRUE
    WHERE id_pemain = NEW.id_pemain;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tambah_pelatih_trigger
BEFORE INSERT ON Pelatih
FOR EACH ROW
EXECUTE FUNCTION validate_pelatih_count();

CREATE TRIGGER penggantian_kapten_trigger
BEFORE UPDATE ON Pemain
FOR EACH ROW
WHEN (NEW.is_captain = TRUE)
EXECUTE FUNCTION set_kapten();