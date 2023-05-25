from django.shortcuts import render

# Create your views here.
def mulaiPertandingan(request):
    return render(request, 'MulaiPertandingan.html')

def peristiwaTim(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        event = request.POST.get('event')
        
        if player_name == 'kartu merah':
            error_message = "Player with 'kartu merah' cannot add more events."
            return render(request, 'CRDMulaiPertandingan/PeristiwaTim.html', {'error_message': error_message})

        if player_name == 'nama pemain' and event == 'Kartu kuning':
            # Check if the player already has one yellow card
            if 'yellow_card_count' in request.session:
                yellow_card_count = request.session['yellow_card_count']
                yellow_card_count += 1

                if yellow_card_count >= 2:
                    player_name = 'kartu merah'
                    error_message = "Player received two yellow cards and converted to 'kartu merah'. Cannot add more events."
                    return render(request, 'yourapp/manage_pertandingan.html', {'error_message': error_message})

                request.session['yellow_card_count'] = yellow_card_count
            else:
                request.session['yellow_card_count'] = 1

    return render(request, 'PeristiwaTim.html')

